"""Global filter state and application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd
import streamlit as st

from streamlit_app.contracts import FILTER_COLUMN_MAP


@dataclass
class FilterState:
    date_start: date
    date_end: date
    stages: list[str]
    industries: list[str]
    account_types: list[str]


def init_filter_state(df: pd.DataFrame) -> None:
    min_date = pd.to_datetime(df[FILTER_COLUMN_MAP["date_range"]]).min().date()
    max_date = pd.to_datetime(df[FILTER_COLUMN_MAP["date_range"]]).max().date()
    st.session_state.setdefault("date_range", (min_date, max_date))
    st.session_state.setdefault("selected_stages", [])
    st.session_state.setdefault("selected_industries", [])
    st.session_state.setdefault("selected_account_types", [])


def read_sidebar_filters(df: pd.DataFrame) -> FilterState:
    init_filter_state(df)
    st.sidebar.header("Global Filters")
    date_range = st.sidebar.date_input(
        "Close Date Range",
        value=st.session_state["date_range"],
    )
    if not isinstance(date_range, tuple) or len(date_range) != 2:
        date_range = st.session_state["date_range"]

    stages = sorted(
        [value for value in df[FILTER_COLUMN_MAP["stage"]].dropna().unique().tolist()]
    )
    industries = sorted(
        [
            value
            for value in df[FILTER_COLUMN_MAP["industry"]].dropna().unique().tolist()
        ]
    )
    account_types = sorted(
        [
            value
            for value in df[FILTER_COLUMN_MAP["account_type"]]
            .dropna()
            .unique()
            .tolist()
        ]
    )

    selected_stages = st.sidebar.multiselect(
        "Stage", stages, default=st.session_state["selected_stages"]
    )
    selected_industries = st.sidebar.multiselect(
        "Industry",
        industries,
        default=st.session_state["selected_industries"],
    )
    selected_account_types = st.sidebar.multiselect(
        "Account Type",
        account_types,
        default=st.session_state["selected_account_types"],
    )

    st.session_state["date_range"] = date_range
    st.session_state["selected_stages"] = selected_stages
    st.session_state["selected_industries"] = selected_industries
    st.session_state["selected_account_types"] = selected_account_types

    return FilterState(
        date_start=date_range[0],
        date_end=date_range[1],
        stages=selected_stages,
        industries=selected_industries,
        account_types=selected_account_types,
    )


def apply_global_filters(df: pd.DataFrame, state: FilterState) -> pd.DataFrame:
    filtered = df.copy()
    date_col = FILTER_COLUMN_MAP["date_range"]
    filtered[date_col] = pd.to_datetime(filtered[date_col])
    filtered = filtered[
        (filtered[date_col].dt.date >= state.date_start)
        & (filtered[date_col].dt.date <= state.date_end)
    ]

    if state.stages:
        filtered = filtered[filtered[FILTER_COLUMN_MAP["stage"]].isin(state.stages)]
    if state.industries:
        filtered = filtered[
            filtered[FILTER_COLUMN_MAP["industry"]].isin(state.industries)
        ]
    if state.account_types:
        filtered = filtered[
            filtered[FILTER_COLUMN_MAP["account_type"]].isin(state.account_types)
        ]

    return filtered
