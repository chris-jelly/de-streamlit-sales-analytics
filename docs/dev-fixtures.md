# Local Dev Fixtures

SQLite dev mode uses deterministic Parquet fixtures stored in `fixtures/sales_seed`.

## Regenerate fixtures

Run:

- `uv run python scripts/generate_dev_fixtures.py`

This overwrites the three canonical fixture files.

## Fixture files

- `fct_salesforce_opportunities.parquet`
- `dim_salesforce_accounts.parquet`
- `opportunity_history_snapshot.parquet`

## Expected shape

### `fct_salesforce_opportunities`

- Core IDs: `opportunity_id`, `account_id`
- Display fields: `opportunity_name`, `account_name`, `stage_name`, `opportunity_type`
- KPI/filter fields: `amount`, `probability`, `close_date`, `is_closed`, `is_won`, `currency_iso_code`
- Freshness fields: `source_last_modified_at`, `raw_extracted_at`

### `dim_salesforce_accounts`

- Core IDs: `account_id`, `account_name`
- Filter fields: `industry`, `account_type`
- Freshness fields: `source_last_modified_at`, `raw_extracted_at`

### `opportunity_history_snapshot`

- Core IDs: `opportunity_id`, `snapshot_date`
- Trend fields: `stage_name`, `amount`, `probability`, `close_date`
- Freshness field: `source_last_modified_at`

## Built-in edge cases

Fixtures intentionally include:

- `industry` null values
- `account_type` null values
- open and closed opportunities
- won and lost opportunities
- probability coverage including 0 and 100
- overdue and future close dates
- zero-amount opportunities
- multiple snapshot dates for trend charts
