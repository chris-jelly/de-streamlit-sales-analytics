# Streamlit Sales Pipeline Pulse (Phase 1)

Internal Streamlit dashboard for Phase 1 sales pipeline analytics.

## Local run

1. Create a Python 3.13+ environment.
2. Install dependencies with uv:
   - `uv sync --extra dev`
3. Set required env var:
   - `SALES_WAREHOUSE_URL` (read-only warehouse connection URL)
4. Run:
   - `uv run streamlit run streamlit_app/app.py`

## Scope

- Three tabs: `Overview`, `Forecast`, `History`
- Canonical marts only:
  - `fct_salesforce_opportunities`
  - `dim_salesforce_accounts`
  - `opportunity_history_snapshot`

See `docs/runtime-contract.md` for runtime/deployment contract details.
