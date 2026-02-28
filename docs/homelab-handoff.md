# Homelab Handoff Inputs

Use this when wiring deployment YAML in `~/git/homelab`.

## Image coordinates

- Registry: `ghcr.io`
- Image: `ghcr.io/chris-jelly/de-streamlit-sales-analytics/streamlit-sales-pipeline-pulse`
- Tags produced by CI:
  - branch tag
  - commit sha tag
  - git tag (for `v*` releases)

## Required secret keys

- `SALES_WAREHOUSE_URL`: SQLAlchemy Postgres DSN/URL for dedicated read-only warehouse user.
  - Expected driver prefix: `postgresql+psycopg://`
  - CNPG service pattern: `postgresql+psycopg://<user>:<password>@<cluster-name>-rw.<namespace>.svc.cluster.local:5432/<database>?sslmode=require`

## Runtime env defaults

- `APP_ENV=prod`
- `APP_TITLE=Sales Pipeline Pulse - Phase 1`
- `STREAMLIT_PORT=8501`
- `STREAMLIT_ADDRESS=0.0.0.0`

## Probe configuration

- Liveness HTTP path: `/_stcore/health`
- Readiness HTTP path: `/_stcore/health`
- Port: `8501`

## Resource request defaults

- CPU request: `250m`
- Memory request: `512Mi`
- CPU limit: intentionally omitted in Phase 1

## Exposure policy

- Internal/trusted network only
- Public ingress disabled for Phase 1
