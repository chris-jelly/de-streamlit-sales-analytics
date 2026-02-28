## 1. Runtime and backend selection

- [x] 1.1 Extend runtime settings to support explicit backend selection for dev (`warehouse` vs `sqlite`) with safe defaults.
- [x] 1.2 Update startup flow to allow no-secret local startup only in dev and preserve fail-fast behavior outside dev.
- [x] 1.3 Introduce a shared data-client contract and wire backend factory selection in `app.py`/data access paths.

## 2. Local fixture assets and loading

- [x] 2.1 Add deterministic fixture generation script that outputs canonical Parquet files for fact/accounts/history without Faker.
- [x] 2.2 Add checked-in Parquet fixture assets and document expected row shape and edge-case coverage.
- [x] 2.3 Implement SQLite bootstrap that loads Parquet fixtures into canonical table names used by dashboard queries.

## 3. Local client behavior and contract validation

- [x] 3.1 Implement `LocalDevClient` methods for fact/history fetches and freshness timestamps matching warehouse client behavior.
- [x] 3.2 Reuse/extend model contract validation so local tables enforce required-column constraints before render.
- [x] 3.3 Add clear error messaging for invalid fixture schema and backend misconfiguration.

## 4. Verification and docs

- [x] 4.1 Add/extend tests for backend routing, local startup without `SALES_WAREHOUSE_URL`, and non-dev fail-fast behavior.
- [x] 4.2 Add tests for local contract validation failures and parity on key KPI/filter/freshness paths.
- [x] 4.3 Update README/runtime docs with local dev commands, backend env vars, and fixture refresh workflow.
