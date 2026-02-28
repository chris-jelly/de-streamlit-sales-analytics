## MODIFIED Requirements

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
