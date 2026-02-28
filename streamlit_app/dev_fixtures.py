"""Deterministic local fixture generation for SQLite-backed dev mode."""

from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

from streamlit_app.contracts import MODEL_NAMES

STAGES = [
    "Prospecting",
    "Qualification",
    "Proposal",
    "Negotiation",
    "Closed Won",
    "Closed Lost",
]
INDUSTRIES = ["Technology", "Finance", "Healthcare", "Retail", "Energy", None]
ACCOUNT_TYPES = ["Customer", "Partner", "Prospect", None]
OPPORTUNITY_TYPES = ["New Business", "Expansion", "Renewal"]


def _build_accounts(total: int = 36) -> pd.DataFrame:
    base_modified = datetime(2026, 2, 15, 8, 0, 0)
    extracted = datetime(2026, 2, 15, 10, 30, 0)
    records: list[dict[str, object]] = []
    for idx in range(total):
        records.append(
            {
                "account_id": f"ACC-{idx + 1:04d}",
                "account_name": f"Account {idx + 1:03d}",
                "account_type": ACCOUNT_TYPES[idx % len(ACCOUNT_TYPES)],
                "industry": INDUSTRIES[idx % len(INDUSTRIES)],
                "source_last_modified_at": base_modified + timedelta(days=idx % 11),
                "raw_extracted_at": extracted,
            }
        )
    return pd.DataFrame.from_records(records)


def _is_closed(stage_name: str) -> bool:
    return stage_name.startswith("Closed")


def _is_won(stage_name: str) -> bool:
    return stage_name == "Closed Won"


def _build_opportunities(total: int = 120) -> pd.DataFrame:
    records: list[dict[str, object]] = []
    base_close_date = date(2025, 12, 15)
    source_base = datetime(2026, 2, 20, 9, 0, 0)
    extracted = datetime(2026, 2, 21, 6, 0, 0)

    for idx in range(total):
        stage_name = STAGES[idx % len(STAGES)]
        amount = float(((idx % 20) + 1) * 7500)
        if idx % 31 == 0:
            amount = 0.0

        probability = float((idx * 13) % 101)
        if stage_name == "Closed Won":
            probability = 100.0
        elif stage_name == "Closed Lost":
            probability = 0.0

        records.append(
            {
                "opportunity_id": f"OPP-{idx + 1:05d}",
                "account_id": f"ACC-{(idx % 36) + 1:04d}",
                "account_name": f"Account {(idx % 36) + 1:03d}",
                "opportunity_name": f"Opportunity {idx + 1:03d}",
                "stage_name": stage_name,
                "amount": amount,
                "probability": probability,
                "close_date": base_close_date + timedelta(days=idx * 4 - 140),
                "opportunity_type": OPPORTUNITY_TYPES[idx % len(OPPORTUNITY_TYPES)],
                "is_closed": _is_closed(stage_name),
                "is_won": _is_won(stage_name),
                "currency_iso_code": "USD",
                "source_last_modified_at": source_base + timedelta(days=idx % 17),
                "raw_extracted_at": extracted,
            }
        )

    return pd.DataFrame.from_records(records)


def _build_history(opportunities: pd.DataFrame) -> pd.DataFrame:
    snapshot_dates = [
        date(2025, 12, 1),
        date(2026, 1, 1),
        date(2026, 2, 1),
        date(2026, 3, 1),
    ]
    stages_by_snapshot = ["Prospecting", "Qualification", "Proposal", "Negotiation"]
    records: list[dict[str, object]] = []
    source_base = datetime(2026, 2, 20, 9, 0, 0)

    for row_idx, row in opportunities.iterrows():
        for snap_idx, snapshot in enumerate(snapshot_dates):
            stage_name = stages_by_snapshot[snap_idx]
            if bool(row["is_closed"]):
                stage_name = "Closed Won" if bool(row["is_won"]) else "Closed Lost"

            amount = float(row["amount"]) * (0.75 + (snap_idx * 0.08))
            if bool(row["is_closed"]):
                amount = float(row["amount"])

            probability = float(row["probability"])
            if not bool(row["is_closed"]):
                probability = min(100.0, max(0.0, probability - 20 + snap_idx * 10))

            records.append(
                {
                    "opportunity_id": row["opportunity_id"],
                    "snapshot_date": snapshot,
                    "stage_name": stage_name,
                    "amount": round(amount, 2),
                    "probability": probability,
                    "close_date": row["close_date"],
                    "source_last_modified_at": source_base
                    + timedelta(days=(row_idx + snap_idx) % 21),
                }
            )

    return pd.DataFrame.from_records(records)


def generate_fixture_frames() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    accounts = _build_accounts()
    opportunities = _build_opportunities()
    history = _build_history(opportunities)
    return opportunities, accounts, history


def write_parquet_fixtures(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    opportunities, accounts, history = generate_fixture_frames()
    opportunities.to_parquet(output_dir / f"{MODEL_NAMES['fact']}.parquet", index=False)
    accounts.to_parquet(output_dir / f"{MODEL_NAMES['accounts']}.parquet", index=False)
    history.to_parquet(output_dir / f"{MODEL_NAMES['history']}.parquet", index=False)
