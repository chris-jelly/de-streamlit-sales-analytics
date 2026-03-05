"""App runtime configuration."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    db_url: str
    warehouse_schema: str
    data_backend: str
    local_fixture_dir: str
    local_sqlite_url: str
    app_env: str
    app_title: str
    streamlit_port: int
    streamlit_address: str


def from_env() -> Settings:
    load_dotenv()
    app_env = os.getenv("APP_ENV", "dev")
    default_backend = "sqlite" if app_env == "dev" else "warehouse"
    default_fixture_dir = (
        Path(__file__).resolve().parent.parent / "fixtures" / "sales_seed"
    )
    default_local_db = (
        Path(__file__).resolve().parent.parent / ".streamlit" / "dev-local.db"
    )
    return Settings(
        db_url=os.getenv("SALES_WAREHOUSE_URL", ""),
        warehouse_schema=os.getenv("WAREHOUSE_SCHEMA", "marts").strip(),
        data_backend=os.getenv("DATA_BACKEND", default_backend).strip().lower(),
        local_fixture_dir=os.getenv("LOCAL_FIXTURE_DIR", str(default_fixture_dir)),
        local_sqlite_url=os.getenv(
            "LOCAL_SQLITE_URL", f"sqlite+pysqlite:///{default_local_db}"
        ),
        app_env=app_env,
        app_title=os.getenv("APP_TITLE", "Sales Pipeline Pulse - Phase 1"),
        streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
        streamlit_address=os.getenv("STREAMLIT_ADDRESS", "0.0.0.0"),
    )
