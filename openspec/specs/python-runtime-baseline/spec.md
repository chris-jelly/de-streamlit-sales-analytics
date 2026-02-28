## Purpose
Define the repository-wide Python runtime baseline contract and dependency-management policy for local development, CI, and container execution.

## Requirements

### Requirement: Repository runtime baseline is Python 3.13 or newer
The repository SHALL declare and use Python 3.13+ as the minimum supported runtime across developer guidance, project metadata, CI execution, and container runtime configuration.

#### Scenario: Runtime declarations are aligned to one baseline
- **WHEN** runtime configuration files are reviewed
- **THEN** Docker runtime, CI interpreter version, packaging metadata, and local-run documentation SHALL all indicate Python 3.13+ as the baseline

### Requirement: Python 3.13 baseline compatibility is continuously verified
The system SHALL verify install and test execution under Python 3.13 through repository automation.

#### Scenario: CI validates Python 3.13 execution path
- **WHEN** repository CI runs for pull requests or default-branch changes
- **THEN** dependencies SHALL install and tests SHALL execute under Python 3.13

### Requirement: uv sync works for local development
The project SHALL support `uv sync` as a working local dependency setup flow under the Python 3.13+ baseline.

#### Scenario: Editable build succeeds during uv sync
- **WHEN** a contributor runs `uv sync` at repository root
- **THEN** dependency resolution and editable project build SHALL complete without package-discovery errors

### Requirement: Dependencies are managed only through uv artifacts
The repository SHALL use `pyproject.toml` and `uv.lock` as the sole dependency management artifacts and SHALL NOT require `requirements.txt`.

#### Scenario: Single source of truth for dependencies
- **WHEN** project dependency files are reviewed
- **THEN** runtime and development dependencies SHALL be declared in `pyproject.toml` and resolved in `uv.lock`

#### Scenario: Legacy requirements file is removed
- **WHEN** the uv migration is complete
- **THEN** `requirements.txt` SHALL be absent from active dependency install workflows

### Requirement: Redundant future-annotations imports are not required
The codebase SHALL treat `from __future__ import annotations` as unnecessary under the Python 3.13+ baseline unless a concrete file-specific need is documented.

#### Scenario: Annotation import policy under modern baseline
- **WHEN** Python modules are updated for the 3.13+ baseline
- **THEN** `from __future__ import annotations` SHALL be removed unless retaining it is explicitly justified for that module
