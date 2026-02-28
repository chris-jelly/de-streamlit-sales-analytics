from __future__ import annotations

import pandas as pd

from streamlit_app.metrics import (
    open_pipeline_amount,
    weighted_pipeline_amount,
    win_rate,
)


def test_open_pipeline_amount_only_open_rows_counted() -> None:
    df = pd.DataFrame(
        {
            "amount": [100.0, 200.0, 300.0],
            "is_closed": [False, True, False],
            "probability": [10, 20, 30],
            "is_won": [False, True, False],
        }
    )
    assert open_pipeline_amount(df) == 400.0


def test_weighted_pipeline_amount_formula() -> None:
    df = pd.DataFrame(
        {
            "amount": [100.0, 250.0],
            "is_closed": [False, False],
            "probability": [10.0, 80.0],
            "is_won": [False, False],
        }
    )
    assert weighted_pipeline_amount(df) == 210.0


def test_win_rate_divide_by_zero_handling() -> None:
    df = pd.DataFrame(
        {
            "amount": [100.0],
            "is_closed": [False],
            "probability": [10.0],
            "is_won": [False],
        }
    )
    assert win_rate(df) == 0.0
