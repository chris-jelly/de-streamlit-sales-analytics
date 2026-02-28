from datetime import datetime

import pandas as pd
import pytest

import streamlit_app.app as app


def test_render_selected_view_executes_only_overview_renderer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = {"overview": 0, "forecast": 0, "history": 0}

    monkeypatch.setattr(app.st, "caption", lambda _: None)
    monkeypatch.setattr(
        app,
        "render_overview",
        lambda _: calls.__setitem__("overview", calls["overview"] + 1),
    )
    monkeypatch.setattr(
        app,
        "render_forecast",
        lambda _: calls.__setitem__("forecast", calls["forecast"] + 1),
    )
    monkeypatch.setattr(
        app,
        "render_history",
        lambda _: calls.__setitem__("history", calls["history"] + 1),
    )

    df = pd.DataFrame({"amount": [1]})
    app.render_selected_view(
        "Overview",
        filtered_fact=df,
        filtered_history=df,
        fact_raw_freshness=datetime(2026, 2, 28, 10, 0, 0),
        history_snapshot_freshness=datetime(2026, 2, 27, 0, 0, 0),
        fallback_freshness=datetime(2026, 2, 26, 0, 0, 0),
    )

    assert calls == {"overview": 1, "forecast": 0, "history": 0}


def test_render_selected_view_executes_only_history_renderer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = {"overview": 0, "forecast": 0, "history": 0}

    monkeypatch.setattr(app.st, "caption", lambda _: None)
    monkeypatch.setattr(
        app,
        "render_overview",
        lambda _: calls.__setitem__("overview", calls["overview"] + 1),
    )
    monkeypatch.setattr(
        app,
        "render_forecast",
        lambda _: calls.__setitem__("forecast", calls["forecast"] + 1),
    )
    monkeypatch.setattr(
        app,
        "render_history",
        lambda _: calls.__setitem__("history", calls["history"] + 1),
    )

    fact_df = pd.DataFrame({"amount": [1]})
    history_df = pd.DataFrame({"amount": [2]})
    app.render_selected_view(
        "History",
        filtered_fact=fact_df,
        filtered_history=history_df,
        fact_raw_freshness=datetime(2026, 2, 28, 10, 0, 0),
        history_snapshot_freshness=datetime(2026, 2, 27, 0, 0, 0),
        fallback_freshness=datetime(2026, 2, 26, 0, 0, 0),
    )

    assert calls == {"overview": 0, "forecast": 0, "history": 1}


def test_render_selected_view_rejects_invalid_name() -> None:
    df = pd.DataFrame({"amount": [1]})
    with pytest.raises(ValueError, match="Unsupported dashboard view"):
        app.render_selected_view(
            "Invalid",
            filtered_fact=df,
            filtered_history=df,
            fact_raw_freshness=datetime(2026, 2, 28, 10, 0, 0),
            history_snapshot_freshness=datetime(2026, 2, 27, 0, 0, 0),
            fallback_freshness=datetime(2026, 2, 26, 0, 0, 0),
        )
