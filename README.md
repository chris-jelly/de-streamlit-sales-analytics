# Streamlit Sales Pipeline Pulse (Phase 1)

Internal Streamlit dashboard for Phase 1 sales pipeline analytics.

## Local run

1. Create a Python 3.13+ environment.
2. Install dependencies with uv:
   - `uv sync --extra dev`
3. Choose a backend mode:
   - **SQLite dev mode (no secret):**
     - Generate deterministic fixtures: `uv run python scripts/generate_dev_fixtures.py`
      - Set env vars:
        - `APP_ENV=dev`
        - `DATA_BACKEND=sqlite`
        - Optional: `LOCAL_FIXTURE_DIR=fixtures/sales_seed`
        - Optional: `LOCAL_SQLITE_URL` (defaults to persistent `.streamlit/dev-local.db`)
   - **Warehouse mode:**
     - Set env vars:
       - `DATA_BACKEND=warehouse`
       - `SALES_WAREHOUSE_URL` (read-only warehouse connection URL)
4. Run the app:
   - `uv run streamlit run streamlit_app/app.py`

See `docs/dev-fixtures.md` for fixture schema shape and edge-case coverage.

## Scope

- Three views: `Overview`, `Forecast`, `History` (single active view rendered per rerun)
- Canonical marts only:
  - `fct_salesforce_opportunities`
  - `dim_salesforce_accounts`
  - `opportunity_history_snapshot`

## UI and theming conventions

- Native Streamlit theming is defined in `.streamlit/config.toml`
- Global filters and app metadata live in the sidebar; charts and tables stay in the main area
- Dashboard sections use bordered card/grouping patterns for consistency

See `docs/runtime-contract.md` for runtime/deployment contract details.
