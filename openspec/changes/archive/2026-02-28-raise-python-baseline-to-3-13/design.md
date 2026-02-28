## Context

The repository currently signals Python support in multiple places (`Dockerfile`, CI workflow, project metadata, and contributor docs), and those signals are not consistently aligned to the desired baseline. The requested direction is Path A: require Python 3.13+ as the floor. The codebase also includes widespread `from __future__ import annotations` usage, which is no longer necessary for postponed evaluation semantics in modern Python baselines and can be standardized as part of the migration.

## Goals / Non-Goals

**Goals:**
- Set a single Python baseline of 3.13+ for container runtime, CI test interpreter, packaging metadata, and local-run documentation.
- Preserve current dashboard behavior while updating runtime contracts.
- Define a clear policy for `from __future__ import annotations` under the 3.13+ baseline and apply it consistently.
- Keep dependency pins installable on Python 3.13 in CI and image builds.
- Standardize container dependency installation on `uv` instead of `pip`.
- Remove `requirements.txt` and use `uv`-native dependency management as the single project workflow.
- Ensure `uv sync` works for contributors by fixing current editable-build/package-discovery failures.

**Non-Goals:**
- Feature-level changes to dashboard tabs, KPI definitions, or filter behavior.
- Reworking dependency strategy beyond compatibility checks needed for Python 3.13.
- Any deployment-manifest changes outside this repository.

## Decisions

1. **Adopt Python 3.13+ as the explicit repository baseline**
   - Decision: Update Docker base image, CI `setup-python` version, project `requires-python`, and README runtime instructions to 3.13+.
   - Rationale: These are the primary sources of truth consumed by developers and automation; aligning them removes ambiguity.
   - Alternative considered: Keep `requires-python >=3.11` while only moving runtime to 3.13.
   - Why not alternative: Transitional support adds policy complexity and conflicts with the selected strict Path A direction.

2. **Treat `from __future__ import annotations` as removable by default**
   - Decision: Remove `from __future__ import annotations` in application and test modules unless a file has a concrete compatibility/tooling need documented in code review.
   - Rationale: Under Python 3.13+, postponed annotation behavior is native, so retaining the future import generally adds noise rather than value.
   - Alternative considered: Keep existing imports for stylistic consistency.
   - Why not alternative: It preserves redundant syntax and weakens the value of standardizing around a modern baseline.

3. **Verify compatibility through existing test/build paths**
   - Decision: Use the repository test workflow and container build path as compatibility gates.
   - Rationale: These paths already model the real execution surfaces for this project.
   - Alternative considered: Introduce a multi-version test matrix.
   - Why not alternative: It is unnecessary after selecting a single required baseline.

4. **Use `uv` for Docker dependency installation**
   - Decision: Install and invoke `uv` in the Docker build and perform dependency installation through `uv`-managed project metadata and lockfile.
   - Rationale: `uv` provides faster, more reproducible dependency installation in container builds and aligns with a single package-management toolchain.
   - Alternative considered: Keep `pip` for simplicity.
   - Why not alternative: It misses the requested tooling standardization and provides weaker performance characteristics for image builds.

5. **Make `uv sync` a supported local workflow**
   - Decision: Update packaging discovery configuration so editable builds succeed when `uv sync` builds the local project package.
   - Rationale: Current `uv sync` fails because setuptools auto-discovers multiple top-level packages (`openspec`, `streamlit_app`) in flat layout.
   - Alternative considered: Keep `uv` for Docker only and ignore local `uv sync` failure.
   - Why not alternative: It creates a split-brain toolchain and leaves a broken developer path in the repo.

6. **Drop `requirements.txt` as a dependency source**
   - Decision: Remove `requirements.txt` and treat `pyproject.toml` + `uv.lock` as the sole dependency declaration and resolution artifacts.
   - Rationale: Maintaining parallel dependency definitions increases drift risk and undermines reproducibility.
   - Alternative considered: Keep generating and committing `requirements.txt` alongside `uv` files.
   - Why not alternative: It introduces dual maintenance and inconsistent install paths across environments.

## Risks / Trade-offs

- **Dependency pin drift for Python 3.13** -> Validate lockstep install in CI and container build; upgrade pins only when a package cannot install or execute on 3.13.
- **Hidden tooling assumptions about 3.11** -> Audit and update obvious references in docs/workflows, and rely on CI failures to surface missed assumptions.
- **Annotation edge cases in static analysis** -> Remove future imports incrementally and confirm tests pass; retain only if a file demonstrates a concrete need.
- **`uv` behavior differences from `pip`** -> Validate install command semantics in Docker and keep a documented fallback path if package resolution differs unexpectedly.
- **Packaging config changes affect build outputs** -> Keep package inclusion explicit and minimal; validate editable build and tests after updating package discovery settings.
- **Lockfile churn in CI and PRs** -> Treat `uv.lock` as a first-class artifact with clear update expectations in contributor docs.

## Migration Plan

1. Update all runtime declarations to Python 3.13+ in Docker, CI, project metadata, and docs.
2. Switch Docker dependency installation from `pip` to `uv` using project metadata and lockfile inputs.
3. Remove `requirements.txt` and complete migration to `pyproject.toml` + `uv.lock` workflows for local, CI, and container paths.
4. Update Python packaging discovery config so `uv sync` completes without multiple-top-level-package errors.
5. Run dependency install and tests on Python 3.13 in CI context.
6. Remove redundant `__future__` annotation imports and re-run test suite.
7. Publish updated container image from the 3.13 base and verify healthcheck behavior remains unchanged.

Rollback strategy:
- Revert runtime declaration changes to 3.11 and restore removed future imports if blocking compatibility issues are discovered.

## Open Questions

- Should contributor docs specify `3.13.x` exactly for reproducibility, or keep `3.13+` language for flexibility?
- Do we want a lightweight lint rule to prevent reintroduction of redundant `from __future__ import annotations` imports?
