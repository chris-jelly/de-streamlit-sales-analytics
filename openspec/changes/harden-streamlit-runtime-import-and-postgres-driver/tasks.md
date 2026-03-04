## 1. Runtime import hardening

- [x] 1.1 Update container/runtime startup so `streamlit_app` package imports are deterministic in the production Streamlit execution path.
- [x] 1.2 Add an automated verification that exercises the real app startup mode and fails on `ModuleNotFoundError: streamlit_app`.

## 2. Warehouse driver dialect alignment

- [x] 2.1 Update warehouse URL handling to strictly require `postgresql+psycopg://` for warehouse mode.
- [x] 2.2 Add validation/error messaging that fails fast for `postgresql://` and `postgresql+psycopg2://` inputs with clear migration guidance.

## 3. Operational readiness and docs

- [x] 3.1 Add startup/import-mode smoke verification that exercises the real Streamlit startup path and fails on `ModuleNotFoundError: streamlit_app`.
- [x] 3.2 Add automated driver-contract tests verifying `postgresql+psycopg://` acceptance and psycopg2-path rejection behavior.
- [x] 3.3 Update runtime contract documentation and deployment handoff notes with strict DSN dialect and startup/import requirements.
- [ ] 3.4 Validate rollout in cluster logs: no `ModuleNotFoundError: streamlit_app` and no `No module named 'psycopg2'`.
