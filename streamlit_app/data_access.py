"""Warehouse access restricted to approved marts."""

from datetime import date, datetime
from pathlib import Path
from typing import Protocol

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import StaticPool

from streamlit_app.config import Settings
from streamlit_app.contracts import JOIN_CONTRACT, MODEL_NAMES, REQUIRED_COLUMNS


class ContractValidationError(RuntimeError):
    """Raised when expected model columns are missing."""


class DataClient(Protocol):
    def validate_model_contracts(self) -> None: ...

    def fetch_current_fact(self, start_date: date, end_date: date) -> pd.DataFrame: ...

    def fetch_history_snapshot(
        self, start_date: date, end_date: date
    ) -> pd.DataFrame: ...

    def freshness_fact_raw_extracted_at(self) -> pd.Timestamp | None: ...

    def freshness_history_snapshot_date(self) -> pd.Timestamp | None: ...

    def freshness_fallback_source_modified(self) -> pd.Timestamp | None: ...


class BaseSqlClient:
    def __init__(
        self, engine: Engine, table_refs: dict[str, str] | None = None
    ) -> None:
        self.engine = engine
        self.table_refs = table_refs or {name: name for name in MODEL_NAMES.values()}

    def _table(self, name: str) -> str:
        return self.table_refs.get(name, name)

    def _query(self, sql: str, params: dict | None = None) -> pd.DataFrame:
        with self.engine.begin() as conn:
            return pd.read_sql_query(text(sql), conn, params=params)

    def validate_model_contracts(self) -> None:
        for model, required_cols in REQUIRED_COLUMNS.items():
            df = self._query(f"select * from {self._table(model)} limit 0")
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
            from {self._table(MODEL_NAMES["fact"])} as f
            left join {self._table(MODEL_NAMES["accounts"])} as a
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
            from {self._table(MODEL_NAMES["history"])} as h
            left join {self._table(MODEL_NAMES["fact"])} as f
                on h.opportunity_id = f.opportunity_id
            left join {self._table(MODEL_NAMES["accounts"])} as a
                on f.{JOIN_CONTRACT["left_key"]} = a.{JOIN_CONTRACT["right_key"]}
            where h.close_date between :start_date and :end_date
            """,
            params={"start_date": start_date, "end_date": end_date},
        )

    def freshness_fact_raw_extracted_at(self) -> pd.Timestamp | None:
        df = self._query(
            f"select max(raw_extracted_at) as freshness_ts from {self._table(MODEL_NAMES['fact'])}"
        )
        return _coerce_ts(df["freshness_ts"][0])

    def freshness_history_snapshot_date(self) -> pd.Timestamp | None:
        df = self._query(
            f"select max(snapshot_date) as freshness_ts from {self._table(MODEL_NAMES['history'])}"
        )
        return _coerce_ts(df["freshness_ts"][0])

    def freshness_fallback_source_modified(self) -> pd.Timestamp | None:
        df = self._query(
            f"select max(source_last_modified_at) as freshness_ts from {self._table(MODEL_NAMES['fact'])}"
        )
        return _coerce_ts(df["freshness_ts"][0])


class WarehouseClient(BaseSqlClient):
    @classmethod
    def from_settings(cls, settings: Settings) -> "WarehouseClient":
        _validate_warehouse_db_url(settings.db_url)
        schema = _validate_warehouse_schema(settings.warehouse_schema)
        table_refs = {name: f"{schema}.{name}" for name in MODEL_NAMES.values()}
        return cls(engine=create_engine(settings.db_url), table_refs=table_refs)


class LocalDevClient(BaseSqlClient):
    @classmethod
    def from_settings(cls, settings: Settings) -> "LocalDevClient":
        engine = _create_sqlite_engine(settings.local_sqlite_url)
        bootstrap_sqlite_from_parquet(engine, Path(settings.local_fixture_dir))
        return cls(engine=engine)


def create_client(settings: Settings) -> DataClient:
    if settings.data_backend == "warehouse":
        return WarehouseClient.from_settings(settings)
    if settings.data_backend == "sqlite":
        if settings.app_env != "dev":
            raise ValueError(
                "DATA_BACKEND=sqlite is only supported when APP_ENV=dev. "
                "Use warehouse backend outside dev."
            )
        return LocalDevClient.from_settings(settings)
    raise ValueError(
        f"Unsupported DATA_BACKEND '{settings.data_backend}'. "
        "Expected one of: warehouse, sqlite."
    )


def bootstrap_sqlite_from_parquet(engine: Engine, fixture_dir: Path) -> None:
    fixture_paths = {
        MODEL_NAMES["fact"]: fixture_dir / f"{MODEL_NAMES['fact']}.parquet",
        MODEL_NAMES["accounts"]: fixture_dir / f"{MODEL_NAMES['accounts']}.parquet",
        MODEL_NAMES["history"]: fixture_dir / f"{MODEL_NAMES['history']}.parquet",
    }

    missing_paths = [
        str(path)
        for path in fixture_paths.values()
        if not path.exists() or not path.is_file()
    ]
    if missing_paths:
        missing_lines = "\n".join(f"- {path}" for path in missing_paths)
        raise ValueError(
            "Missing local fixture parquet files. Expected:\n"
            f"{missing_lines}\n"
            "Set LOCAL_FIXTURE_DIR to a valid fixture directory or run scripts/generate_dev_fixtures.py."
        )

    with engine.begin() as conn:
        for table_name, parquet_path in fixture_paths.items():
            frame = pd.read_parquet(parquet_path)
            frame.to_sql(table_name, conn, if_exists="replace", index=False)


def _create_sqlite_engine(sqlite_url: str) -> Engine:
    if ":memory:" in sqlite_url:
        return create_engine(
            sqlite_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    return create_engine(sqlite_url)


def _validate_warehouse_db_url(db_url: str) -> None:
    if not db_url:
        raise ValueError("SALES_WAREHOUSE_URL is required")

    required_prefix = "postgresql+psycopg://"
    if db_url.startswith(required_prefix):
        return

    if db_url.startswith("postgresql://"):
        raise ValueError(
            "SALES_WAREHOUSE_URL must use postgresql+psycopg:// (psycopg v3). "
            "Replace postgresql:// with postgresql+psycopg://."
        )

    if db_url.startswith("postgresql+psycopg2://"):
        raise ValueError(
            "SALES_WAREHOUSE_URL must use postgresql+psycopg:// (psycopg v3). "
            "postgresql+psycopg2:// is not supported."
        )

    raise ValueError("SALES_WAREHOUSE_URL must use postgresql+psycopg:// (psycopg v3).")


def _validate_warehouse_schema(schema: str) -> str:
    normalized = schema.strip()
    if not normalized:
        raise ValueError("WAREHOUSE_SCHEMA is required when DATA_BACKEND=warehouse")

    if not normalized.replace("_", "").isalnum():
        raise ValueError(
            "WAREHOUSE_SCHEMA must be a simple SQL identifier (letters, numbers, underscores)."
        )

    return normalized


def _coerce_ts(value: object) -> pd.Timestamp | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, pd.Timestamp):
        return value
    if not isinstance(value, (str, int, float, date, datetime)):
        return None
    parsed = pd.to_datetime([value], errors="coerce")[0]
    if pd.isna(parsed):
        return None
    if not isinstance(parsed, pd.Timestamp):
        return None
    return parsed
