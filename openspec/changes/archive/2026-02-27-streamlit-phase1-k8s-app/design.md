## Context

Phase 1 requires an internal-only Streamlit dashboard that serves canonical sales pipeline analytics and can be built as a container from this repository. Source requirements are already drafted in the Phase 1 spec documents, and this change operationalizes those requirements as an implementable app + CI baseline. The homelab deployment manifests in `~/git/homelab` are intentionally out of scope; this design defines the runtime contract that those manifests will consume.

## Goals / Non-Goals

**Goals:**
- Deliver a Streamlit app with fixed Phase 1 tab structure (`Overview`, `Forecast`, `History`) and canonical KPI/visual semantics.
- Isolate data access behind a query/service layer that only reads approved marts.
- Provide reproducible container builds in GitHub Actions for deployment consumption.
- Define Kubernetes runtime expectations: internal-only ingress intent, ESO-based secret inputs, health probes, and resource requests.

**Non-Goals:**
- Author or apply cluster/environment deployment manifests in `~/git/homelab`.
- Add SSO, HA, autoscaling, alerting, owner-level analytics, or contact analytics.
- Introduce direct dependencies on raw or intermediate warehouse models.

## Decisions

1. Build app as a modular Streamlit package with separate layers for UI composition, metrics logic, and data access.
   - Rationale: keeps UI implementation simple while preserving testability and enforcing canonical KPI/filter behavior in one place.
   - Alternative considered: all logic directly inside Streamlit page files; rejected because metric/query drift across tabs becomes likely.

2. Enforce canonical marts through explicit query contracts and shared data-access helpers.
   - Rationale: prevents accidental coupling to non-approved datasets and keeps lineage aligned with Phase 1 constraints.
   - Alternative considered: ad-hoc SQL in each tab; rejected due to governance and maintenance risk.

3. Use global filter state in Streamlit session state and bind all tab renderers to a shared filtered dataset contract.
   - Rationale: ensures cross-tab consistency and avoids duplicated filtering rules.
   - Alternative considered: per-tab independent filters; rejected because it violates requirement for consistent global filter behavior.

4. Build and publish container images via GitHub Actions using repository-managed Docker assets.
   - Rationale: provides a repeatable build artifact and clean handoff to homelab deployment workflows.
   - Alternative considered: local-only image builds; rejected because it does not support reliable team delivery.

5. Represent runtime expectations as app-facing Kubernetes contract values (env vars, probes, resources, ingress assumptions) without coupling to homelab manifests.
   - Rationale: cleanly separates app delivery from environment-specific deployment definitions.
   - Alternative considered: include full homelab manifests in this change; rejected as out of scope and repository-boundary mismatch.

6. Lock Phase 1 data contracts to concrete dbt mart columns from `~/git/de-airflow-pipeline/dags/dbt/models/marts`.
   - Rationale: removes ambiguity before implementation and aligns app logic with existing marts.
   - Contract mapping:
     - Global filters: `fct_salesforce_opportunities.close_date`, `fct_salesforce_opportunities.stage_name`, `dim_salesforce_accounts.industry`, `dim_salesforce_accounts.account_type`.
     - KPI inputs: `fct_salesforce_opportunities.amount`, `fct_salesforce_opportunities.probability`, `fct_salesforce_opportunities.is_closed`, `fct_salesforce_opportunities.is_won`.
     - History/trends: `opportunity_history_snapshot.snapshot_date`, `opportunity_history_snapshot.stage_name`, `opportunity_history_snapshot.amount`, `opportunity_history_snapshot.probability`, `opportunity_history_snapshot.close_date`.
     - Join key: `fct_salesforce_opportunities.account_id = dim_salesforce_accounts.account_id`.
   - Alternative considered: infer columns at runtime from warehouse metadata; rejected because it creates runtime fragility and weakens testability.

7. Standardize freshness indicator semantics by source reliability.
   - Rationale: `raw_extracted_at` best represents ingestion recency for current-state marts and is available on fact/dim models.
   - Rule:
     - For `Overview` and `Forecast`, freshness timestamp = `max(fct_salesforce_opportunities.raw_extracted_at)`.
     - For `History`, freshness timestamp = `max(opportunity_history_snapshot.snapshot_date)`.
     - If any primary freshness field is null/unavailable, fallback to `max(fct_salesforce_opportunities.source_last_modified_at)` and render an "approximate freshness" label.
   - Alternative considered: one single freshness timestamp for all tabs from `source_last_modified_at`; rejected because it does not reflect snapshot-table recency accurately.

## Risks / Trade-offs

- Data model drift between marts and app assumptions -> Mitigation: centralize query definitions and add smoke checks for required columns.
- Streamlit state complexity across tabs -> Mitigation: define a single filter schema object and shared update/apply helpers.
- CI image build failures from dependency or base-image changes -> Mitigation: pin base image and key dependencies, and run build checks on PRs.
- Runtime contract mismatch with homelab manifests -> Mitigation: document required env vars/secrets and probe endpoints in implementation docs/tasks.
- Freshness confusion across current-state vs snapshot views -> Mitigation: enforce tab-specific freshness rule and UI labeling for fallback behavior.

## Migration Plan

1. Implement app modules and local run path with canonical data queries.
2. Add containerization assets and GitHub Actions build workflow to publish tagged images.
3. Validate runtime contract (health endpoint behavior, secret/env names, resource request defaults).
4. Hand off required deployment values to homelab repository for environment-specific manifests.

Rollback approach: if a release fails, deploy the prior image tag while preserving existing secret/env contracts.

## Open Questions

- Which container registry and image naming convention should GitHub Actions publish to for homelab consumption?
- What exact secret key names should be standardized between this repo and External Secrets Operator mappings in homelab?
