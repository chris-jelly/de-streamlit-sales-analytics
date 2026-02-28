## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Runtime contract declares Python 3.13+ baseline
The Phase 1 runtime contract SHALL explicitly document Python 3.13+ as the minimum supported runtime for this dashboard.

#### Scenario: Runtime contract version statement exists
- **WHEN** runtime contract and onboarding docs are reviewed
- **THEN** they SHALL state that Python 3.13+ is required for local and container execution
