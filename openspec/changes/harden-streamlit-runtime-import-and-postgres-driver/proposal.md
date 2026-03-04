## Why

The production container can pass basic health checks while the Streamlit app fails at runtime due to Python execution-context imports and warehouse driver dialect mismatch. This needs to be fixed now to restore reliable cluster operation and prevent false-positive deploy health.

## What Changes

- Define and enforce a runtime startup contract that guarantees `streamlit_app` imports succeed in the actual Streamlit execution path used in production.
- Define and enforce warehouse DSN dialect compatibility with the installed PostgreSQL driver stack (`psycopg` v3), preventing fallback imports of `psycopg2`.
- Add verification gates for both transport health and functional app/query readiness so readiness reflects real user-facing behavior.
- Update runtime documentation and deployment handoff expectations to include startup/import and DSN requirements.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `streamlit-phase1-dashboard`: tighten runtime execution and warehouse connectivity requirements so production readiness includes import-stable app launch and driver-compatible DB access.

## Impact

- Affected code/assets: `Dockerfile`, Streamlit startup/runtime path, config/env parsing for warehouse URL handling, readiness/validation logic, and runtime docs.
- Affected systems: repository CI/container verification and homelab deployment runtime contract.
- Dependencies: no new runtime library expected; behavior aligns with existing `psycopg[binary]` dependency.
