## Context

The current app startup path assumes warehouse connectivity and stops immediately when `SALES_WAREHOUSE_URL` is absent. This is appropriate for deployed environments but slows local iteration, because developers cannot render the dashboard without secrets and network access. The change introduces a local backend path that preserves existing dashboard behavior and contracts while removing the credential dependency in `APP_ENV=dev`.

Constraints:
- Existing production/stage behavior must remain warehouse-first and unchanged.
- Existing canonical mart schemas and filter/KPI contracts must continue to apply in local mode.
- Local fixture data should be deterministic so UI output and tests are stable across runs.

## Goals / Non-Goals

**Goals:**
- Enable no-secret local startup by routing dev mode to SQLite backed by checked-in Parquet fixtures.
- Preserve canonical model contracts via the existing validation flow in both warehouse and local backends.
- Keep app rendering logic unchanged by exposing one shared client interface.
- Make fixture generation repeatable and deterministic without introducing Faker.

**Non-Goals:**
- Replacing warehouse usage in non-dev environments.
- Introducing new analytical views, KPI formulas, or filter semantics.
- Creating production data migration workflows; this only affects local development and test ergonomics.

## Decisions

### Decision: Backend routing is environment-aware and explicit
- **Choice:** Introduce backend selection in runtime settings, defaulting to warehouse unless local dev conditions are met.
- **Rationale:** Minimizes production behavior changes while allowing deterministic local fallback.
- **Alternatives considered:**
  - Always fallback to local if `SALES_WAREHOUSE_URL` is missing: rejected because silent fallback in non-dev environments could hide misconfiguration.
  - Add only manual CLI switches: rejected because app behavior should remain self-contained via configuration.

### Decision: SQLite runtime with Parquet seed assets
- **Choice:** Store deterministic fixture data as Parquet files, then load into a local SQLite database used by a `LocalDevClient`.
- **Rationale:** Parquet is compact and typed for source-of-truth fixtures; SQLite preserves SQL query behavior close to warehouse paths.
- **Alternatives considered:**
  - CSV-only fixtures loaded directly to pandas: rejected because it bypasses SQL path validation.
  - In-memory generated data only: rejected because deterministic reviewed fixture assets are easier to audit and maintain.

### Decision: Preserve a shared client contract
- **Choice:** Both warehouse and local clients expose the same fetch/freshness/validation methods consumed by `app.py`.
- **Rationale:** Keeps UI code and cached loading functions stable while swapping data backends beneath.
- **Alternatives considered:**
  - Conditional query code in `app.py`: rejected because it spreads backend concerns into UI orchestration.

### Decision: Keep contract validation strict in dev
- **Choice:** Run required-column validation against local tables before data loads.
- **Rationale:** Detects fixture drift early and ensures local mode remains representative of canonical marts.
- **Alternatives considered:**
  - Warning-only validation in dev: rejected because failures become latent until later integration.

## Risks / Trade-offs

- **Fixture staleness versus canonical marts** -> Mitigation: include a documented fixture regeneration step and deterministic generation script.
- **SQLite SQL compatibility drift from warehouse engine** -> Mitigation: keep local queries simple and aligned with the current query subset; cover backend parity in tests.
- **Parquet read/write dependency overhead** -> Mitigation: use lightweight, common Parquet engine dependency and keep fixture files small.
- **Configuration ambiguity (dev backend selection)** -> Mitigation: document precedence rules (`APP_ENV`, backend mode, DB URL presence) in README/runtime docs.

## Migration Plan

1. Add local backend configuration fields and route selection logic.
2. Implement deterministic fixture generator and checked-in Parquet files for fact/accounts/history.
3. Implement SQLite loader + `LocalDevClient` with the shared client interface.
4. Update app startup to permit no-secret startup in dev and preserve current behavior elsewhere.
5. Add tests for backend selection, contract validation in local mode, and parity of key fetch/freshness paths.
6. Update onboarding docs with local run commands and fixture maintenance guidance.

Rollback strategy: remove local backend selection and continue requiring `SALES_WAREHOUSE_URL`; fixture files/scripts can remain inert or be removed in a follow-up cleanup.

## Open Questions

- Should backend selection use a dedicated variable (for example `DATA_BACKEND=warehouse|sqlite`) in addition to `APP_ENV`, or rely solely on `APP_ENV` + URL presence?
- Should fixture refresh be a committed script-only workflow, or include a CI guard that validates fixtures were regenerated from source definitions?
- Should dev startup create SQLite in-memory for speed or use a persistent local file for easier inspection/debugging?
