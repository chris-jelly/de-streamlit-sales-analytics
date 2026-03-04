from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from streamlit_app.config import Settings, from_env
from streamlit_app.contracts import MODEL_NAMES
from streamlit_app.data_access import (
    ContractValidationError,
    LocalDevClient,
    create_client,
)
from streamlit_app.dev_fixtures import generate_fixture_frames


def _write_fixture_dir(path: Path, *, drop_fact_column: str | None = None) -> None:
    fact, accounts, history = generate_fixture_frames()
    if drop_fact_column is not None:
        fact = fact.drop(columns=[drop_fact_column])
    path.mkdir(parents=True, exist_ok=True)
    fact.to_parquet(path / f"{MODEL_NAMES['fact']}.parquet", index=False)
    accounts.to_parquet(path / f"{MODEL_NAMES['accounts']}.parquet", index=False)
    history.to_parquet(path / f"{MODEL_NAMES['history']}.parquet", index=False)


def test_from_env_defaults_backend_by_app_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.delenv("DATA_BACKEND", raising=False)
    assert from_env().data_backend == "sqlite"

    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.delenv("DATA_BACKEND", raising=False)
    assert from_env().data_backend == "warehouse"


def test_create_client_local_sqlite_in_dev_without_warehouse_url(
    tmp_path: Path,
) -> None:
    fixture_dir = tmp_path / "fixtures"
    _write_fixture_dir(fixture_dir)
    settings = Settings(
        db_url="",
        data_backend="sqlite",
        local_fixture_dir=str(fixture_dir),
        local_sqlite_url="sqlite+pysqlite:///:memory:",
        app_env="dev",
        app_title="Test",
        streamlit_port=8501,
        streamlit_address="0.0.0.0",
    )

    client = create_client(settings)
    assert isinstance(client, LocalDevClient)
    client.validate_model_contracts()

    fact = client.fetch_current_fact(date(2025, 1, 1), date(2027, 1, 1))
    history = client.fetch_history_snapshot(date(2025, 1, 1), date(2027, 1, 1))
    assert not fact.empty
    assert not history.empty
    assert client.freshness_fact_raw_extracted_at() is not None
    assert client.freshness_history_snapshot_date() is not None
    assert client.freshness_fallback_source_modified() is not None


def test_create_client_rejects_sqlite_backend_outside_dev(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    _write_fixture_dir(fixture_dir)
    settings = Settings(
        db_url="",
        data_backend="sqlite",
        local_fixture_dir=str(fixture_dir),
        local_sqlite_url="sqlite+pysqlite:///:memory:",
        app_env="prod",
        app_title="Test",
        streamlit_port=8501,
        streamlit_address="0.0.0.0",
    )

    with pytest.raises(ValueError, match="only supported when APP_ENV=dev"):
        create_client(settings)


def test_create_client_requires_warehouse_url_for_warehouse_backend() -> None:
    settings = Settings(
        db_url="",
        data_backend="warehouse",
        local_fixture_dir="fixtures/sales_seed",
        local_sqlite_url="sqlite+pysqlite:///:memory:",
        app_env="dev",
        app_title="Test",
        streamlit_port=8501,
        streamlit_address="0.0.0.0",
    )

    with pytest.raises(ValueError, match="SALES_WAREHOUSE_URL is required"):
        create_client(settings)


def test_create_client_accepts_psycopg3_warehouse_url() -> None:
    settings = Settings(
        db_url="postgresql+psycopg://user:pass@warehouse.example.com:5432/sales",
        data_backend="warehouse",
        local_fixture_dir="fixtures/sales_seed",
        local_sqlite_url="sqlite+pysqlite:///:memory:",
        app_env="prod",
        app_title="Test",
        streamlit_port=8501,
        streamlit_address="0.0.0.0",
    )

    client = create_client(settings)
    assert client is not None


@pytest.mark.parametrize(
    ("warehouse_url", "expected_error"),
    [
        (
            "postgresql://user:pass@warehouse.example.com:5432/sales",
            "Replace postgresql:// with postgresql",
        ),
        (
            "postgresql+psycopg2://user:pass@warehouse.example.com:5432/sales",
            "psycopg2:// is not supported",
        ),
    ],
)
def test_create_client_rejects_non_psycopg3_warehouse_urls(
    warehouse_url: str,
    expected_error: str,
) -> None:
    settings = Settings(
        db_url=warehouse_url,
        data_backend="warehouse",
        local_fixture_dir="fixtures/sales_seed",
        local_sqlite_url="sqlite+pysqlite:///:memory:",
        app_env="prod",
        app_title="Test",
        streamlit_port=8501,
        streamlit_address="0.0.0.0",
    )

    with pytest.raises(ValueError, match=expected_error):
        create_client(settings)


def test_local_contract_validation_fails_for_missing_required_columns(
    tmp_path: Path,
) -> None:
    fixture_dir = tmp_path / "fixtures"
    _write_fixture_dir(fixture_dir, drop_fact_column="probability")
    settings = Settings(
        db_url="",
        data_backend="sqlite",
        local_fixture_dir=str(fixture_dir),
        local_sqlite_url="sqlite+pysqlite:///:memory:",
        app_env="dev",
        app_title="Test",
        streamlit_port=8501,
        streamlit_address="0.0.0.0",
    )

    client = create_client(settings)
    with pytest.raises(ContractValidationError, match="missing required columns"):
        client.validate_model_contracts()


def test_local_bootstrap_errors_when_fixture_files_missing(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"foo": [1]}).to_parquet(fixture_dir / "foo.parquet", index=False)
    settings = Settings(
        db_url="",
        data_backend="sqlite",
        local_fixture_dir=str(fixture_dir),
        local_sqlite_url="sqlite+pysqlite:///:memory:",
        app_env="dev",
        app_title="Test",
        streamlit_port=8501,
        streamlit_address="0.0.0.0",
    )

    with pytest.raises(ValueError, match="Missing local fixture parquet files"):
        create_client(settings)
