"""Canonical model and field contracts for Phase 1."""

MODEL_NAMES = {
    "fact": "fct_salesforce_opportunities",
    "accounts": "dim_salesforce_accounts",
    "history": "opportunity_history_snapshot",
}

REQUIRED_COLUMNS = {
    MODEL_NAMES["fact"]: {
        "opportunity_id",
        "account_id",
        "opportunity_name",
        "stage_name",
        "amount",
        "probability",
        "close_date",
        "is_closed",
        "is_won",
        "source_last_modified_at",
        "raw_extracted_at",
    },
    MODEL_NAMES["accounts"]: {
        "account_id",
        "account_name",
        "account_type",
        "industry",
        "source_last_modified_at",
        "raw_extracted_at",
    },
    MODEL_NAMES["history"]: {
        "opportunity_id",
        "snapshot_date",
        "stage_name",
        "amount",
        "probability",
        "close_date",
        "source_last_modified_at",
    },
}

FILTER_COLUMN_MAP = {
    "date_range": "close_date",
    "stage": "stage_name",
    "industry": "industry",
    "account_type": "account_type",
}

JOIN_CONTRACT = {
    "left_model": MODEL_NAMES["fact"],
    "left_key": "account_id",
    "right_model": MODEL_NAMES["accounts"],
    "right_key": "account_id",
}
