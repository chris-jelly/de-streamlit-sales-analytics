## Purpose
Define local development SQLite fixture behavior for the dashboard so contributors can run and validate analytics flows without warehouse secrets.

## Requirements

### Requirement: Local dev mode SHALL run without warehouse secrets
The system SHALL allow the dashboard to start in local development mode without `SALES_WAREHOUSE_URL` by using a local SQLite backend.

#### Scenario: Dev startup without warehouse URL
- **WHEN** `APP_ENV=dev` and no warehouse URL is configured
- **THEN** the app SHALL initialize a local SQLite-backed data client and SHALL NOT stop with a missing-secret error

#### Scenario: Non-dev startup without warehouse URL
- **WHEN** runtime is not in dev mode and no warehouse URL is configured
- **THEN** the app SHALL fail fast with a clear configuration error

### Requirement: Local fixtures SHALL be deterministic and canonical
The system SHALL provide deterministic local fixture assets for the canonical mart models used by the dashboard.

#### Scenario: Fixture asset set is complete
- **WHEN** local fixture assets are prepared
- **THEN** they SHALL include records for `fct_salesforce_opportunities`, `dim_salesforce_accounts`, and `opportunity_history_snapshot`

#### Scenario: Fixture generation is repeatable
- **WHEN** fixture generation is executed repeatedly from the same source logic
- **THEN** the produced Parquet data SHALL be deterministic in schema and values

### Requirement: Local backend SHALL enforce model contracts
The local SQLite backend SHALL validate canonical required-column contracts before rendering dashboard views.

#### Scenario: Required columns present
- **WHEN** local fixture-backed tables satisfy required columns
- **THEN** model contract validation SHALL pass and data loading SHALL proceed

#### Scenario: Required columns missing
- **WHEN** a local fixture-backed table is missing one or more required columns
- **THEN** the app SHALL fail with a contract validation error that identifies missing columns

### Requirement: Dashboard behavior SHALL remain backend-agnostic
The dashboard view orchestration SHALL produce equivalent filter/KPI/freshness behavior regardless of warehouse or local backend selection.

#### Scenario: Shared client contract for data access
- **WHEN** the app loads fact, history, and freshness data
- **THEN** both warehouse and local backends SHALL satisfy the same client interface consumed by dashboard rendering flow
