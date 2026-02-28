## 1. Project Setup and App Skeleton

- [x] 1.1 Create the Streamlit app package structure and entrypoint for `Overview`, `Forecast`, and `History` tabs.
- [x] 1.2 Add and pin required Python dependencies for Streamlit, data access, and chart rendering.
- [x] 1.3 Add environment/config loading for warehouse connectivity and runtime metadata.

## 2. Data Access and Canonical Metrics

- [x] 2.1 Implement a shared data-access layer that queries only `fct_salesforce_opportunities`, `dim_salesforce_accounts`, and `opportunity_history_snapshot`.
- [x] 2.2 Implement explicit field mappings for filters and joins (`close_date`, `stage_name`, `industry`, `account_type`, and `account_id` join key).
- [x] 2.3 Implement canonical KPI calculation helpers for open pipeline, weighted pipeline, and win rate (with divide-by-zero handling).
- [x] 2.4 Add validation/smoke checks for required mart columns and graceful error handling for missing fields.

## 3. Global Filters and UI Rendering

- [x] 3.1 Implement shared global filters (date range, stage, industry, account type) in Streamlit session state.
- [x] 3.2 Build `Overview` tab visuals: KPI cards, stage distribution, and opportunities table using shared metric/filter helpers.
- [x] 3.3 Build `Forecast` tab visuals: weighted pipeline by close month and close-date bucket views.
- [x] 3.4 Build `History` tab visuals: pipeline trend, weighted pipeline trend, and daily movers.
- [x] 3.5 Add tab-specific freshness logic: `Overview`/`Forecast` use `max(raw_extracted_at)` from fact, `History` uses `max(snapshot_date)` from snapshot.
- [x] 3.6 Implement freshness fallback to `max(source_last_modified_at)` with an explicit "approximate" UI label when fallback is used.

## 4. Runtime Contract and Containerization

- [x] 4.1 Add containerization assets (Dockerfile and supporting files) for the Streamlit app runtime.
- [x] 4.2 Define runtime contract values for secret/env inputs, liveness/readiness behavior, and default resource requests.
- [x] 4.3 Document internal-only ingress intent and explicitly note that homelab deployment manifests are out of scope for this change.

## 5. GitHub Actions Build Pipeline

- [x] 5.1 Add a GitHub Actions workflow that builds the app container image on default branch/release triggers.
- [x] 5.2 Configure image tagging and publish steps for the target registry used by homelab deployment manifests.
- [x] 5.3 Add pipeline checks/logging to verify build reproducibility and publish success criteria.

## 6. Verification and Handoff

- [x] 6.1 Add automated tests for canonical KPI logic, filter field-to-column mapping, and cross-tab consistency behavior.
- [x] 6.2 Add automated tests for freshness selection and fallback labeling behavior across tabs.
- [x] 6.3 Run local app and CI validation to confirm all required Phase 1 visuals and runtime constraints are satisfied.
- [x] 6.4 Produce handoff notes listing required secret keys, image coordinates, and deployment contract inputs for `~/git/homelab`.
