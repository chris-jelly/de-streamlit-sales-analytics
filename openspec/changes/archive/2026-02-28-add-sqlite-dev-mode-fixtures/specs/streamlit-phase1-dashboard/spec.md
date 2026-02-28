## MODIFIED Requirements

### Requirement: Secrets and database access follow least privilege
The app SHALL use least-privilege credentials for warehouse access in deployed environments and SHALL support secretless local development through deterministic SQLite fixtures.

#### Scenario: Read-only warehouse credentials
- **WHEN** database credentials are provisioned for the app
- **THEN** they SHALL be a dedicated read-only warehouse user for analytics queries

#### Scenario: Secret delivery mechanism
- **WHEN** app runtime secrets are provided in Kubernetes
- **THEN** they SHALL be delivered via External Secrets Operator-managed Kubernetes Secrets

#### Scenario: Secretless local development mode
- **WHEN** the app runs in local development mode without warehouse credentials
- **THEN** the dashboard SHALL run using deterministic local fixture data and SHALL NOT require secret delivery infrastructure
