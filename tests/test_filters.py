from __future__ import annotations

from datetime import date

import pandas as pd

from streamlit_app.contracts import FILTER_COLUMN_MAP
from streamlit_app.filters import FilterState, apply_global_filters


def test_filter_column_mapping_contract() -> None:
    assert FILTER_COLUMN_MAP["date_range"] == "close_date"
    assert FILTER_COLUMN_MAP["stage"] == "stage_name"
    assert FILTER_COLUMN_MAP["industry"] == "industry"
    assert FILTER_COLUMN_MAP["account_type"] == "account_type"


def test_apply_global_filters_cross_tab_consistent_predicates() -> None:
    df = pd.DataFrame(
        {
            "close_date": pd.to_datetime(["2026-01-10", "2026-01-20", "2026-02-15"]),
            "stage_name": ["Prospecting", "Closed Won", "Prospecting"],
            "industry": ["Tech", "Finance", "Tech"],
            "account_type": ["Customer", "Partner", "Customer"],
        }
    )
    state = FilterState(
        date_start=date(2026, 1, 1),
        date_end=date(2026, 1, 31),
        stages=["Prospecting"],
        industries=["Tech"],
        account_types=["Customer"],
    )
    filtered = apply_global_filters(df, state)
    assert len(filtered) == 1
    assert filtered.iloc[0]["stage_name"] == "Prospecting"
