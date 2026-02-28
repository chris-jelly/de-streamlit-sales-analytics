# Streamlit Sales Pipeline Pulse - Phase 1 Spec Draft

## ADDED Requirements

### Requirement: Phase 1 internal dashboard scope
The system SHALL provide a Phase 1 Streamlit dashboard for internal sales pipeline analytics with a constrained MVP scope.

#### Scenario: Dashboard information architecture is constrained
- **WHEN** Phase 1 is implemented
- **THEN** the app SHALL include exactly three primary tabs: `Overview`, `Forecast`, and `History`

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
The dashboard SHALL apply a shared filter model across tabs and visuals.

#### Scenario: Supported global filters
- **WHEN** the app is in use
- **THEN** global filters SHALL include date range, stage, industry, and account type

#### Scenario: Cross-tab filter consistency
- **WHEN** a user updates any global filter
- **THEN** all relevant charts, KPI cards, and tables across tabs SHALL update consistently


### Requirement: Data freshness is visible
The dashboard SHALL show users when underlying data was last refreshed.

#### Scenario: Freshness timestamp is displayed
- **WHEN** any dashboard page is viewed
- **THEN** a visible freshness indicator SHALL show the most recent available data timestamp used by the app


### Requirement: Kubernetes deployment is internal-only for Phase 1
The app SHALL be deployed to Kubernetes with internal-only ingress exposure for Phase 1.

#### Scenario: Internal-only ingress
- **WHEN** ingress is configured for Phase 1
- **THEN** exposure SHALL be limited to internal/trusted network access and SHALL NOT be publicly exposed without an explicit future scope change


### Requirement: Secrets and database access follow least privilege
The app SHALL use External Secrets Operator and least-privilege credentials for warehouse access.

#### Scenario: Read-only warehouse credentials
- **WHEN** database credentials are provisioned for the app
- **THEN** they SHALL be a dedicated read-only warehouse user for analytics queries

#### Scenario: Secret delivery mechanism
- **WHEN** app runtime secrets are provided in Kubernetes
- **THEN** they SHALL be delivered via External Secrets Operator-managed Kubernetes Secrets


### Requirement: Baseline runtime operability is included
The Phase 1 deployment SHALL include basic runtime health and resource requests.

#### Scenario: Health probes are configured
- **WHEN** the Kubernetes deployment is reviewed
- **THEN** liveness and readiness probes SHALL be configured for the Streamlit service

#### Scenario: Resource requests are configured
- **WHEN** the Kubernetes deployment is reviewed
- **THEN** CPU and memory requests SHALL be set for the app container

#### Scenario: CPU limits are not required in Phase 1
- **WHEN** Phase 1 resource policy is applied
- **THEN** CPU limits SHALL NOT be required by this spec
