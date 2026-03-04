## ADDED Requirements

### Requirement: Production app startup is import-stable
The Phase 1 dashboard runtime SHALL guarantee `streamlit_app` package imports succeed in the production Streamlit execution path.

#### Scenario: Streamlit app startup resolves package imports
- **WHEN** the production image runs the configured Streamlit entry command
- **THEN** app startup SHALL complete without `ModuleNotFoundError: streamlit_app`

#### Scenario: Startup contract remains stable across execution contexts
- **WHEN** runtime execution context details (entrypoint, script/module invocation semantics, or working directory behavior) vary within supported deployment usage
- **THEN** the runtime contract SHALL still provide a deterministic import path for the `streamlit_app` package

### Requirement: Warehouse dialect maps to installed PostgreSQL driver
When warehouse backend mode is enabled, the runtime SHALL use a SQLAlchemy PostgreSQL dialect that is compatible with installed `psycopg` v3 dependencies.

#### Scenario: Psycopg v3 dialect is required
- **WHEN** `DATA_BACKEND=warehouse` and `SALES_WAREHOUSE_URL` is provided
- **THEN** the URL SHALL use the `postgresql+psycopg://` dialect prefix

#### Scenario: Warehouse URL does not trigger psycopg2 fallback imports
- **WHEN** `DATA_BACKEND=warehouse` and `SALES_WAREHOUSE_URL` is provided
- **THEN** runtime database client initialization SHALL NOT require `psycopg2`

#### Scenario: Incompatible warehouse URL surfaces actionable startup error
- **WHEN** warehouse URL input is incompatible with the runtime-supported driver dialect
- **THEN** the app SHALL fail fast with a configuration error that explains the expected PostgreSQL dialect/driver format

#### Scenario: Bare PostgreSQL dialect is rejected
- **WHEN** `SALES_WAREHOUSE_URL` uses `postgresql://` without an explicit driver
- **THEN** app startup SHALL fail with guidance to use `postgresql+psycopg://`

#### Scenario: Psycopg2 dialect is rejected
- **WHEN** `SALES_WAREHOUSE_URL` uses `postgresql+psycopg2://`
- **THEN** app startup SHALL fail with guidance that only `postgresql+psycopg://` is supported

### Requirement: Verification covers startup and driver contract regressions
Phase 1 verification SHALL include targeted checks for import-context startup behavior and PostgreSQL driver contract behavior.

#### Scenario: Deploy validation includes real app startup path
- **WHEN** release validation is executed for the container image
- **THEN** verification SHALL include the same startup path used by the Streamlit app runtime, not only module-based health commands

#### Scenario: Driver contract test accepts psycopg v3 URL
- **WHEN** automated validation runs for warehouse URL handling
- **THEN** `postgresql+psycopg://` inputs SHALL be accepted

#### Scenario: Driver contract test rejects psycopg2 path
- **WHEN** automated validation runs for warehouse URL handling
- **THEN** URLs that would route to `psycopg2` import behavior SHALL be rejected
