## Why

The dashboard currently requires `SALES_WAREHOUSE_URL` at startup, which blocks local development, UI iteration, and contributor onboarding when warehouse credentials are unavailable. We need a deterministic local mode so engineers can run and test the app without secrets while preserving the existing production contract.

## What Changes

- Add a development data backend that runs the app against local SQLite when warehouse connection settings are unavailable in dev.
- Introduce deterministic Parquet fixture assets for the canonical marts (`fact`, `accounts`, `history`) and load them into SQLite for local runs.
- Keep model contract validation active in local mode so required columns and join/filter assumptions fail fast when fixtures drift.
- Update runtime configuration and app startup behavior to route between warehouse and local backends without changing dashboard views.
- Add tests and documentation for backend selection, fixture loading, and no-secret local startup.

## Capabilities

### New Capabilities
- `local-dev-sqlite-fixtures`: Run the Streamlit dashboard locally against deterministic Parquet-backed SQLite fixtures with no warehouse secret.

### Modified Capabilities
- `streamlit-phase1-dashboard`: Expand runtime behavior to support backend selection in dev while preserving existing canonical marts behavior for warehouse-backed environments.

## Impact

- Affected code: `streamlit_app/config.py`, `streamlit_app/app.py`, `streamlit_app/data_access.py`, new fixture-loading module(s), tests, and run documentation.
- New data assets: checked-in Parquet fixture files for canonical models used by the dashboard.
- Dependencies: no new runtime infrastructure; optional Python dependency may be required for Parquet I/O if not already available.
- Systems: local development workflow and CI smoke/testing paths can run without external warehouse connectivity.
