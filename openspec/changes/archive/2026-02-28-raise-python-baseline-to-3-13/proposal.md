## Why

The repository currently mixes Python version signals, with container runtime and CI pinned to 3.11 while the project intends to move to a newer baseline. Standardizing on Python 3.13+ now reduces drift across local development, CI, and container deployment, and keeps the runtime aligned with current ecosystem support.

## What Changes

- Raise the runtime baseline to Python 3.13+ across container, CI, and contributor documentation.
- Update project metadata to declare Python 3.13+ as the supported floor.
- Adopt `uv` as the canonical package manager for this repository (local and container workflows).
- Remove `requirements.txt` and manage dependencies through `pyproject.toml` plus `uv.lock`.
- Make `uv sync` succeed in the repository by resolving current packaging discovery errors.
- Evaluate whether `from __future__ import annotations` is still needed under the new baseline and remove it where redundant.

## Capabilities

### New Capabilities
- `python-runtime-baseline`: Define and enforce a single supported Python runtime baseline (3.13+) across development, CI, and container execution.

### Modified Capabilities
- `streamlit-phase1-dashboard`: Update runtime contract and CI/container requirements to require Python 3.13+ and document annotation import policy under that baseline.

## Impact

- Affected code/assets: `Dockerfile`, `.github/workflows/container-build.yml`, `pyproject.toml`, `README.md`, Python packaging configuration, and Python modules/tests that currently use `from __future__ import annotations`.
- Dependencies: project dependencies must be declared in `pyproject.toml`, resolved in `uv.lock`, and installable on Python 3.13 in CI and container builds.
- Systems: local developer setup, GitHub Actions test job, and published container image runtime; container build tooling now depends on `uv`.
