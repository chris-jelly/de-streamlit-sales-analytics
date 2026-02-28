# Runtime Contract (Phase 1)

This repository defines the app runtime contract consumed by homelab deployment manifests.

## Runtime baseline

- Python: `3.13+`
- Dependency manager: `uv` (`pyproject.toml` + `uv.lock`)

## Environment and secrets

- `SALES_WAREHOUSE_URL` (required): read-only warehouse connection URL.
- `APP_ENV` (optional, default `dev`)
- `APP_TITLE` (optional, default `Sales Pipeline Pulse - Phase 1`)
- `STREAMLIT_PORT` (optional, default `8501`)
- `STREAMLIT_ADDRESS` (optional, default `0.0.0.0`)

Secrets are expected to be provided by External Secrets Operator in Kubernetes.

## Health probes

- Liveness path: `/_stcore/health`
- Readiness path: `/_stcore/health`
- Container healthcheck command: `python -m streamlit_app.health`

Suggested probe defaults:

- Initial delay: 20s
- Period seconds: 30s
- Timeout seconds: 5s
- Failure threshold: 3

## Resource requests

Suggested starting requests:

- CPU: `250m`
- Memory: `512Mi`

CPU limits are intentionally not required for Phase 1.

## Ingress intent

Ingress is internal-only for Phase 1. Public internet exposure is out of scope.

## Out of scope

- Homelab deployment manifests in `~/git/homelab`
- SSO, HA, autoscaling, alerting
