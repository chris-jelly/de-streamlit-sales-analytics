"""Canonical KPI calculations for Phase 1."""

import pandas as pd


def open_pipeline_amount(df: pd.DataFrame) -> float:
    open_df = df[df["is_closed"] == False]  # noqa: E712
    return float(open_df["amount"].fillna(0).sum())


def weighted_pipeline_amount(df: pd.DataFrame) -> float:
    open_df = df[df["is_closed"] == False]  # noqa: E712
    weighted = open_df["amount"].fillna(0) * (open_df["probability"].fillna(0) / 100.0)
    return float(weighted.sum())


def win_rate(df: pd.DataFrame) -> float:
    closed_df = df[df["is_closed"] == True]  # noqa: E712
    denominator = int(len(closed_df))
    if denominator == 0:
        return 0.0
    numerator = int((closed_df["is_won"] == True).sum())  # noqa: E712
    return float(numerator / denominator)


def kpis(df: pd.DataFrame) -> dict[str, float]:
    return {
        "open_pipeline_amount": open_pipeline_amount(df),
        "weighted_pipeline_amount": weighted_pipeline_amount(df),
        "win_rate": win_rate(df),
        "open_opportunity_count": float((df["is_closed"] == False).sum()),  # noqa: E712
    }
