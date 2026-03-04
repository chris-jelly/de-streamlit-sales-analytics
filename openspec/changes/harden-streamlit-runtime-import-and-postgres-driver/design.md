## Context

Cluster evidence shows two separate runtime defects in production behavior. First, script-context execution (`python streamlit_app/app.py` and `streamlit run streamlit_app/app.py`) fails package imports with `ModuleNotFoundError: streamlit_app`, while module-context execution (`python -m streamlit_app.app`) resolves imports successfully. Second, warehouse execution later fails on `ModuleNotFoundError: psycopg2`, indicating DSN dialect/driver mismatch against the installed `psycopg` v3 dependency.

The current runtime contract allows a false-positive state where transport-level health appears green while user-facing app execution remains broken. The design must harden startup/import and warehouse connectivity semantics without introducing unnecessary platform complexity.

## Goals / Non-Goals

**Goals:**
- Make production app startup import-stable for the actual Streamlit execution path.
- Ensure warehouse URL handling is compatible with the installed PostgreSQL driver path and does not attempt `psycopg2` imports.
- Align readiness verification with user-visible functionality (app launch + query path), not only transport health.
- Keep deployment and handoff contracts explicit so homelab rollout is predictable.

**Non-Goals:**
- Redesign Phase 1 dashboard features, metrics, or UI behavior.
- Introduce new data platforms, authentication, or infra topology changes.
- Add new runtime dependencies unless strictly required.

## Decisions

1. Runtime import hardening SHALL prioritize reliability over build-layer micro-optimization.
   - Rationale: this project is small and production correctness is more important than preserving a dependency-only Docker cache optimization.
   - Preferred direction: include local project installation in image dependency sync so package imports are stable regardless of script/module execution semantics.
   - Alternative considered: keep `--no-install-project` and rely on strict runtime path/entrypoint guarantees. Rejected due to brittleness across execution contexts.

2. Warehouse DSN handling SHALL enforce a `psycopg`-compatible dialect contract.
   - Rationale: current runtime includes psycopg v3, and plain `postgresql://` can resolve to `psycopg2` import paths in common SQLAlchemy configurations.
   - Preferred direction: require explicit `postgresql+psycopg://` URLs and fail fast with actionable errors for bare `postgresql://` or `postgresql+psycopg2://` inputs.
   - Alternative considered: adding `psycopg2` to runtime dependencies. Rejected to avoid unnecessary dual-driver support and ambiguity.
   - Alternative considered: auto-normalize `postgresql://` to `postgresql+psycopg://`. Rejected to avoid hidden behavior and preserve explicit runtime contracts.

3. Verification scope SHALL be minimal and targeted to the two known failure classes.
   - Rationale: we need reliable regression coverage without introducing heavy environment-coupled checks.
   - Preferred direction: add (a) startup/import-mode smoke in the real Streamlit execution path and (b) URL/driver contract tests that verify psycopg v3 acceptance and psycopg2-path rejection.
   - Alternative considered: full query-path integration checks in this change. Deferred to keep this hardening change focused and low-friction.

## Risks / Trade-offs

- [Slightly slower dependency-layer cache reuse] -> Mitigation: accept small image-build cost in exchange for deterministic runtime imports.
- [Stricter DSN validation may break previously tolerated URLs] -> Mitigation: document migration rule and provide clear startup error guidance.
- [Minimal verification may miss some environment-specific DB issues] -> Mitigation: keep deploy smoke checks operationally, and add deeper integration checks in a separate change if needed.

## Migration Plan

1. Update runtime/image contract to ensure project package importability in production execution path.
2. Update warehouse URL contract and validation semantics for `psycopg`-compatible dialect.
3. Update docs/runtime handoff guidance with required startup and DSN rules.
4. Add/adjust CI verification to assert app startup/import-mode behavior and strict DSN/driver validation behavior.
5. Roll out image update to homelab and verify logs are free of `streamlit_app` and `psycopg2` module import errors.

Rollback: deploy previous known-good image tag and restore prior env contract while preserving gathered diagnostics.

## Open Questions

- None for this change. Decisions are fixed to strict DSN enforcement and minimal targeted verification.
