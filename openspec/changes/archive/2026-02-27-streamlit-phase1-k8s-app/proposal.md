## Why

The project needs a production-oriented Phase 1 Streamlit app that can run in Kubernetes and expose consistent sales pipeline analytics using canonical mart models. Defining the app and CI container build flow now enables delivery in this repo while keeping homelab deployment wiring in `~/git/homelab` as a separate follow-up.

## What Changes

- Add a Streamlit Phase 1 dashboard with three tabs (`Overview`, `Forecast`, `History`) and the required KPI, chart, and table views.
- Standardize data access to approved mart models only and enforce canonical KPI formulas and shared global filters.
- Add visible data freshness indicators in the UI for operational trust.
- Add containerization and GitHub Actions image build workflow so the app is buildable and publishable from this repository.
- Add Kubernetes-ready runtime configuration artifacts in this repo to define app expectations (health checks, resource requests, internal-only exposure, and ESO-based secret consumption), while leaving homelab environment deployment manifests out of scope.

## Capabilities

### New Capabilities
- `streamlit-phase1-dashboard`: Internal sales pipeline dashboard capability covering Phase 1 UI scope, canonical mart-backed analytics behavior, runtime/container readiness, and Kubernetes operational requirements for implementation in this repository.

### Modified Capabilities
- None.

## Impact

- Affected code: new Streamlit application modules, data query layer, metric/filter helpers, container build assets, and CI workflow files.
- Affected systems: data warehouse read-only analytics access, GitHub Actions build pipeline, and Kubernetes runtime contract consumed by homelab deployment configuration.
- Dependencies: Streamlit, plotting/data libraries, container build tooling, and secret/env contract alignment with External Secrets Operator.
