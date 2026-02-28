"""App runtime configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    db_url: str
    app_env: str
    app_title: str
    streamlit_port: int
    streamlit_address: str


def from_env() -> Settings:
    load_dotenv()
    return Settings(
        db_url=os.getenv("SALES_WAREHOUSE_URL", ""),
        app_env=os.getenv("APP_ENV", "dev"),
        app_title=os.getenv("APP_TITLE", "Sales Pipeline Pulse - Phase 1"),
        streamlit_port=int(os.getenv("STREAMLIT_PORT", "8501")),
        streamlit_address=os.getenv("STREAMLIT_ADDRESS", "0.0.0.0"),
    )
