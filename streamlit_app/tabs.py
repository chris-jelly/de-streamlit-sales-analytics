"""Tab renderers for the Streamlit dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from streamlit_app.metrics import kpis


def render_overview(df: pd.DataFrame) -> None:
    metrics = kpis(df)
    with st.container(horizontal=True):
        with st.container(border=True):
            st.metric("Open Pipeline", f"${metrics['open_pipeline_amount']:,.0f}")
        with st.container(border=True):
            st.metric(
                "Weighted Pipeline", f"${metrics['weighted_pipeline_amount']:,.0f}"
            )
        with st.container(border=True):
            st.metric("Win Rate", f"{metrics['win_rate'] * 100:.1f}%")
        with st.container(border=True):
            st.metric("Open Opportunities", f"{metrics['open_opportunity_count']:,.0f}")

    stage_counts = (
        df.groupby("stage_name", dropna=False).size().reset_index(name="count")
    )
    with st.container(border=True):
        stage_fig = px.bar(
            stage_counts, x="stage_name", y="count", title="Stage Distribution"
        )
        st.plotly_chart(stage_fig, use_container_width=True)

    table_columns = [
        "opportunity_name",
        "account_name",
        "stage_name",
        "amount",
        "probability",
        "close_date",
        "industry",
        "account_type",
    ]
    with st.container(border=True):
        st.subheader("Opportunities")
        st.dataframe(
            df[table_columns].sort_values("close_date", ascending=True),
            use_container_width=True,
        )


def render_forecast(df: pd.DataFrame) -> None:
    forecast = df[df["is_closed"] == False].copy()  # noqa: E712
    forecast["close_month"] = (
        pd.to_datetime(forecast["close_date"]).dt.to_period("M").dt.to_timestamp()
    )
    forecast["weighted_amount"] = forecast["amount"].fillna(0) * (
        forecast["probability"].fillna(0) / 100.0
    )

    month_agg = forecast.groupby("close_month", dropna=False, as_index=False)[
        "weighted_amount"
    ].sum()
    with st.container(border=True):
        month_fig = px.bar(
            month_agg,
            x="close_month",
            y="weighted_amount",
            title="Weighted Pipeline by Close Month",
        )
        st.plotly_chart(month_fig, use_container_width=True)

    today = pd.Timestamp.utcnow().normalize()
    days_to_close = (pd.to_datetime(forecast["close_date"]) - today).dt.days
    forecast["close_date_bucket"] = pd.cut(
        days_to_close,
        bins=[-10_000, -1, 30, 60, 90, 100_000],
        labels=["Overdue", "0-30 days", "31-60 days", "61-90 days", "90+ days"],
    )
    bucket_agg = forecast.groupby("close_date_bucket", dropna=False, as_index=False)[
        "weighted_amount"
    ].sum()
    with st.container(border=True):
        bucket_fig = px.bar(
            bucket_agg,
            x="close_date_bucket",
            y="weighted_amount",
            title="Weighted Pipeline by Close-Date Bucket",
        )
        st.plotly_chart(bucket_fig, use_container_width=True)


def render_history(df: pd.DataFrame) -> None:
    history = df.copy()
    history["snapshot_date"] = pd.to_datetime(history["snapshot_date"])
    history["weighted_amount"] = history["amount"].fillna(0) * (
        history["probability"].fillna(0) / 100.0
    )

    pipeline_trend = history.groupby("snapshot_date", as_index=False)["amount"].sum()
    weighted_trend = history.groupby("snapshot_date", as_index=False)[
        "weighted_amount"
    ].sum()

    with st.container(border=True):
        trend_fig = px.line(
            pipeline_trend, x="snapshot_date", y="amount", title="Pipeline Trend"
        )
        st.plotly_chart(trend_fig, use_container_width=True)

    with st.container(border=True):
        weighted_fig = px.line(
            weighted_trend,
            x="snapshot_date",
            y="weighted_amount",
            title="Weighted Pipeline Trend",
        )
        st.plotly_chart(weighted_fig, use_container_width=True)

    movers = _daily_movers(history)
    with st.container(border=True):
        st.subheader("Daily Movers")
        st.dataframe(movers, use_container_width=True)


def _daily_movers(history: pd.DataFrame) -> pd.DataFrame:
    if history.empty:
        return pd.DataFrame(
            columns=["opportunity_id", "snapshot_date", "amount_delta"]
        )  # pragma: no cover
    sorted_history = history.sort_values(["opportunity_id", "snapshot_date"]).copy()
    sorted_history["previous_amount"] = sorted_history.groupby("opportunity_id")[
        "amount"
    ].shift(1)
    sorted_history["amount_delta"] = sorted_history["amount"] - sorted_history[
        "previous_amount"
    ].fillna(0)
    latest_snapshot = sorted_history["snapshot_date"].max()
    latest = sorted_history[sorted_history["snapshot_date"] == latest_snapshot]
    columns = [
        "opportunity_id",
        "stage_name",
        "amount",
        "previous_amount",
        "amount_delta",
    ]
    return latest[columns].sort_values("amount_delta", ascending=False).head(20)
