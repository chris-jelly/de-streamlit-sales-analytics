"""Phase 1 Streamlit sales pipeline dashboard."""

from datetime import date, timedelta

import pandas as pd
import streamlit as st

from streamlit_app.config import from_env
from streamlit_app.data_access import ContractValidationError, WarehouseClient
from streamlit_app.filters import apply_global_filters, read_sidebar_filters
from streamlit_app.freshness import format_freshness, select_freshness
from streamlit_app.tabs import render_forecast, render_history, render_overview


@st.cache_resource
def get_client() -> WarehouseClient:
    settings = from_env()
    return WarehouseClient.from_settings(settings)


@st.cache_data(ttl=300)
def load_data(start_date: date, end_date: date) -> tuple[pd.DataFrame, pd.DataFrame]:
    client = get_client()
    fact = client.fetch_current_fact(start_date=start_date, end_date=end_date)
    history = client.fetch_history_snapshot(start_date=start_date, end_date=end_date)
    return fact, history


def main() -> None:
    settings = from_env()
    st.set_page_config(page_title=settings.app_title, layout="wide")
    st.title(settings.app_title)

    if not settings.db_url:
        st.error(
            "Missing SALES_WAREHOUSE_URL. Configure secrets/env before running the dashboard."
        )
        st.stop()

    client = get_client()
    try:
        client.validate_model_contracts()
    except ContractValidationError as exc:
        st.error(f"Model contract validation failed: {exc}")
        st.stop()

    default_end = date.today() + timedelta(days=365)
    default_start = date.today() - timedelta(days=365)
    fact_df, history_df = load_data(start_date=default_start, end_date=default_end)

    if fact_df.empty:
        st.warning("No records returned from canonical marts for current date window.")
        st.stop()

    filter_state = read_sidebar_filters(fact_df)
    filtered_fact = apply_global_filters(fact_df, filter_state)
    filtered_history = apply_global_filters(history_df, filter_state)

    fact_raw_freshness = client.freshness_fact_raw_extracted_at()
    history_snapshot_freshness = client.freshness_history_snapshot_date()
    fallback_freshness = client.freshness_fallback_source_modified()

    tab_overview, tab_forecast, tab_history = st.tabs(
        ["Overview", "Forecast", "History"]
    )

    with tab_overview:
        freshness = select_freshness(
            "Overview",
            fact_raw_freshness,
            history_snapshot_freshness,
            fallback_freshness,
        )
        st.caption(format_freshness(freshness))
        render_overview(filtered_fact)

    with tab_forecast:
        freshness = select_freshness(
            "Forecast",
            fact_raw_freshness,
            history_snapshot_freshness,
            fallback_freshness,
        )
        st.caption(format_freshness(freshness))
        render_forecast(filtered_fact)

    with tab_history:
        freshness = select_freshness(
            "History",
            fact_raw_freshness,
            history_snapshot_freshness,
            fallback_freshness,
        )
        st.caption(format_freshness(freshness))
        render_history(filtered_history)


if __name__ == "__main__":
    main()
