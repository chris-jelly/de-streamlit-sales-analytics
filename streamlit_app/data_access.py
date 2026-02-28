"""Warehouse access restricted to approved marts."""

from __future__ import annotations

from datetime import date

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from streamlit_app.config import Settings
from streamlit_app.contracts import JOIN_CONTRACT, MODEL_NAMES, REQUIRED_COLUMNS


class ContractValidationError(RuntimeError):
    """Raised when expected model columns are missing."""


class WarehouseClient:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @classmethod
    def from_settings(cls, settings: Settings) -> "WarehouseClient":
        if not settings.db_url:
            raise ValueError("SALES_WAREHOUSE_URL is required")
        return cls(engine=create_engine(settings.db_url))

    def _query(self, sql: str, params: dict | None = None) -> pd.DataFrame:
        with self.engine.begin() as conn:
            return pd.read_sql_query(text(sql), conn, params=params)

    def validate_model_contracts(self) -> None:
        for model, required_cols in REQUIRED_COLUMNS.items():
            df = self._query(f"select * from {model} limit 0")
            missing = required_cols.difference(set(df.columns))
            if missing:
                missing_cols = ", ".join(sorted(missing))
                raise ContractValidationError(
                    f"Model '{model}' missing required columns: {missing_cols}"
                )

    def fetch_current_fact(self, start_date: date, end_date: date) -> pd.DataFrame:
        return self._query(
            f"""
            select
                f.opportunity_id,
                f.account_id,
                f.account_name,
                f.opportunity_name,
                f.stage_name,
                f.amount,
                f.probability,
                f.close_date,
                f.opportunity_type,
                f.is_closed,
                f.is_won,
                f.currency_iso_code,
                f.source_last_modified_at,
                f.raw_extracted_at,
                a.industry,
                a.account_type
            from {MODEL_NAMES["fact"]} as f
            left join {MODEL_NAMES["accounts"]} as a
                on f.{JOIN_CONTRACT["left_key"]} = a.{JOIN_CONTRACT["right_key"]}
            where f.close_date between :start_date and :end_date
            """,
            params={"start_date": start_date, "end_date": end_date},
        )

    def fetch_history_snapshot(self, start_date: date, end_date: date) -> pd.DataFrame:
        return self._query(
            f"""
            select
                h.opportunity_id,
                h.snapshot_date,
                h.stage_name,
                h.amount,
                h.probability,
                h.close_date,
                h.source_last_modified_at,
                f.account_id,
                a.industry,
                a.account_type
            from {MODEL_NAMES["history"]} as h
            left join {MODEL_NAMES["fact"]} as f
                on h.opportunity_id = f.opportunity_id
            left join {MODEL_NAMES["accounts"]} as a
                on f.{JOIN_CONTRACT["left_key"]} = a.{JOIN_CONTRACT["right_key"]}
            where h.close_date between :start_date and :end_date
            """,
            params={"start_date": start_date, "end_date": end_date},
        )

    def freshness_fact_raw_extracted_at(self) -> pd.Timestamp | None:
        df = self._query(
            f"select max(raw_extracted_at) as freshness_ts from {MODEL_NAMES['fact']}"
        )
        return _coerce_ts(df["freshness_ts"][0])

    def freshness_history_snapshot_date(self) -> pd.Timestamp | None:
        df = self._query(
            f"select max(snapshot_date) as freshness_ts from {MODEL_NAMES['history']}"
        )
        return _coerce_ts(df["freshness_ts"][0])

    def freshness_fallback_source_modified(self) -> pd.Timestamp | None:
        df = self._query(
            f"select max(source_last_modified_at) as freshness_ts from {MODEL_NAMES['fact']}"
        )
        return _coerce_ts(df["freshness_ts"][0])


def _coerce_ts(value: object) -> pd.Timestamp | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, pd.Timestamp):
        return value
    return pd.to_datetime(value)
