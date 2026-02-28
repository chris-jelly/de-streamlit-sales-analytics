## Purpose
Define the Phase 1 internal Streamlit dashboard capability, including canonical analytics behavior and Kubernetes runtime expectations.

## Requirements

### Requirement: Phase 1 internal dashboard scope
The system SHALL provide a Phase 1 Streamlit dashboard for internal sales pipeline analytics with a constrained MVP scope.

#### Scenario: Dashboard information architecture is constrained
- **WHEN** Phase 1 is implemented
- **THEN** the app SHALL expose exactly three primary analytical views named `Overview`, `Forecast`, and `History`, and SHALL activate only one heavy view renderer at a time

#### Scenario: MVP visual scope is constrained
- **WHEN** Phase 1 is implemented
- **THEN** `Overview` SHALL include KPI cards, stage distribution, and an opportunities table; `Forecast` SHALL include weighted pipeline by close month and close-date buckets; `History` SHALL include pipeline trend, weighted pipeline trend, and daily movers

#### Scenario: Explicit non-goals for Phase 1
- **WHEN** Phase 1 scope is reviewed
- **THEN** owner-level analytics, contact analytics, autoscaling, SSO, HA, and alerting SHALL be out of scope

### Requirement: App consumes only canonical marts
The dashboard SHALL consume only approved analytics-ready mart models from the data platform.

#### Scenario: Approved source models only
- **WHEN** app queries are defined
- **THEN** they SHALL read from `fct_salesforce_opportunities`, `dim_salesforce_accounts`, and `opportunity_history_snapshot` only

#### Scenario: No raw or intermediate dependency
- **WHEN** app query lineage is reviewed
- **THEN** the app SHALL NOT directly depend on raw landing tables or dbt intermediate models

### Requirement: Canonical KPI definitions are explicit
The dashboard SHALL use documented canonical metric definitions for all Phase 1 KPI cards.

#### Scenario: Open pipeline amount definition
- **WHEN** open pipeline is calculated
- **THEN** it SHALL be the sum of `amount` where `is_closed = false`

#### Scenario: Weighted pipeline amount definition
- **WHEN** weighted pipeline is calculated
- **THEN** it SHALL be the sum of `amount * (probability / 100.0)` for open opportunities

#### Scenario: Win rate definition
- **WHEN** win rate is calculated
- **THEN** it SHALL be `count(is_won = true) / count(is_closed = true)` with divide-by-zero handling

#### Scenario: KPI contract consistency
- **WHEN** KPI values are rendered in cards and charts
- **THEN** all views SHALL use the same canonical formulas and filter semantics

### Requirement: Global filter behavior is consistent
The dashboard SHALL apply a shared filter model across views and visuals.

#### Scenario: Supported global filters
- **WHEN** the app is in use
- **THEN** global filters SHALL include date range, stage, industry, and account type

#### Scenario: Global filters map to canonical mart fields
- **WHEN** filter predicates are applied
- **THEN** date range SHALL use `fct_salesforce_opportunities.close_date`, stage SHALL use `fct_salesforce_opportunities.stage_name`, industry SHALL use `dim_salesforce_accounts.industry`, and account type SHALL use `dim_salesforce_accounts.account_type`

#### Scenario: Cross-view filter consistency
- **WHEN** a user updates any global filter
- **THEN** all relevant charts, KPI cards, and tables across `Overview`, `Forecast`, and `History` SHALL update consistently

### Requirement: Data freshness is visible
The dashboard SHALL show users when underlying data was last refreshed.

#### Scenario: Freshness timestamp is displayed
- **WHEN** any dashboard page is viewed
- **THEN** a visible freshness indicator SHALL show the most recent available data timestamp used by the app

#### Scenario: Freshness source is deterministic by tab
- **WHEN** freshness is rendered for `Overview` or `Forecast`
- **THEN** the app SHALL use `max(fct_salesforce_opportunities.raw_extracted_at)` as the freshness timestamp

#### Scenario: Snapshot-based freshness for history tab
- **WHEN** freshness is rendered for `History`
- **THEN** the app SHALL use `max(opportunity_history_snapshot.snapshot_date)` as the freshness timestamp

#### Scenario: Freshness fallback is explicitly labeled
- **WHEN** the primary freshness field is null or unavailable
- **THEN** the app SHALL fallback to `max(fct_salesforce_opportunities.source_last_modified_at)` and SHALL label the freshness indicator as approximate

### Requirement: Container image build is managed in repository CI
The system SHALL provide a CI workflow in this repository to build a deployable Streamlit container image for Phase 1 using a Python 3.13+ runtime baseline.

#### Scenario: CI builds deployable image
- **WHEN** the default branch or a release build is triggered
- **THEN** the repository workflow SHALL build the Streamlit app container image from repository Docker assets

#### Scenario: Build artifact is publishable for homelab deployment
- **WHEN** CI build succeeds
- **THEN** the produced image SHALL be tagged and published to the configured registry for consumption by homelab deployment manifests

#### Scenario: CI test job enforces runtime floor
- **WHEN** repository tests run in CI
- **THEN** the workflow SHALL execute tests using Python 3.13 or newer

#### Scenario: Container build uses uv for dependency installation
- **WHEN** the Streamlit container image is built from repository Docker assets
- **THEN** Python dependencies SHALL be installed with `uv` rather than `pip`, using repository `pyproject.toml` and `uv.lock` as dependency sources

### Requirement: Runtime contract declares Python 3.13+ baseline
The Phase 1 runtime contract SHALL explicitly document Python 3.13+ as the minimum supported runtime for this dashboard.

#### Scenario: Runtime contract version statement exists
- **WHEN** runtime contract and onboarding docs are reviewed
- **THEN** they SHALL state that Python 3.13+ is required for local and container execution

### Requirement: Kubernetes runtime contract is internal-only for Phase 1
The app runtime contract SHALL target Kubernetes with internal-only ingress exposure for Phase 1.

#### Scenario: Internal-only ingress intent is defined
- **WHEN** runtime configuration for ingress is documented or templated in this repository
- **THEN** exposure SHALL be limited to internal/trusted network access and SHALL NOT assume public internet exposure

#### Scenario: Homelab deployment manifests remain out of scope
- **WHEN** this change is implemented
- **THEN** environment-specific deployment YAML in `~/git/homelab` SHALL be excluded from this change

### Requirement: Secrets and database access follow least privilege
The app SHALL use External Secrets Operator integration and least-privilege credentials for warehouse access.

#### Scenario: Read-only warehouse credentials
- **WHEN** database credentials are provisioned for the app
- **THEN** they SHALL be a dedicated read-only warehouse user for analytics queries

#### Scenario: Secret delivery mechanism
- **WHEN** app runtime secrets are provided in Kubernetes
- **THEN** they SHALL be delivered via External Secrets Operator-managed Kubernetes Secrets

### Requirement: Baseline runtime operability is included
The Phase 1 runtime contract SHALL include basic health and resource requests for Kubernetes deployment.

#### Scenario: Health probes are configured
- **WHEN** the Kubernetes runtime contract is reviewed
- **THEN** liveness and readiness probes SHALL be defined for the Streamlit service

#### Scenario: Resource requests are configured
- **WHEN** the Kubernetes runtime contract is reviewed
- **THEN** CPU and memory requests SHALL be set for the app container

#### Scenario: CPU limits are not required in Phase 1
- **WHEN** Phase 1 resource policy is applied
- **THEN** CPU limits SHALL NOT be required by this spec
