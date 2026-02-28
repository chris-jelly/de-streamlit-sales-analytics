from datetime import datetime

from streamlit_app.freshness import format_freshness, select_freshness


def test_overview_uses_fact_raw_extracted() -> None:
    fact_ts = datetime(2026, 2, 27, 10, 0, 0)
    result = select_freshness(
        "Overview",
        fact_raw_extracted_max=fact_ts,
        history_snapshot_max=datetime(2026, 2, 27, 0, 0, 0),
        fallback_source_modified_max=None,
    )
    assert result.timestamp == fact_ts
    assert result.is_approximate is False


def test_history_uses_snapshot_date() -> None:
    history_ts = datetime(2026, 2, 26, 0, 0, 0)
    result = select_freshness(
        "History",
        fact_raw_extracted_max=None,
        history_snapshot_max=history_ts,
        fallback_source_modified_max=datetime(2026, 2, 25, 23, 0, 0),
    )
    assert result.timestamp == history_ts
    assert result.is_approximate is False


def test_freshness_fallback_marked_approximate() -> None:
    fallback_ts = datetime(2026, 2, 25, 23, 0, 0)
    result = select_freshness(
        "Forecast",
        fact_raw_extracted_max=None,
        history_snapshot_max=None,
        fallback_source_modified_max=fallback_ts,
    )
    assert result.timestamp == fallback_ts
    assert result.is_approximate is True
    assert "approximate" in format_freshness(result)
