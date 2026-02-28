"""Freshness policy selection and formatting."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FreshnessResult:
    timestamp: datetime | None
    label: str
    is_approximate: bool


def select_freshness(
    tab_name: str,
    fact_raw_extracted_max: datetime | None,
    history_snapshot_max: datetime | None,
    fallback_source_modified_max: datetime | None,
) -> FreshnessResult:
    primary: datetime | None
    if tab_name in {"Overview", "Forecast"}:
        primary = fact_raw_extracted_max
        source_label = "raw extracted"
    else:
        primary = history_snapshot_max
        source_label = "snapshot"

    if primary is not None:
        return FreshnessResult(
            timestamp=primary, label=f"Freshness ({source_label})", is_approximate=False
        )

    return FreshnessResult(
        timestamp=fallback_source_modified_max,
        label="Freshness (approximate from source_last_modified_at)",
        is_approximate=True,
    )


def format_freshness(result: FreshnessResult) -> str:
    if result.timestamp is None:
        return f"{result.label}: unavailable"
    return f"{result.label}: {result.timestamp.isoformat(sep=' ', timespec='seconds')}"
