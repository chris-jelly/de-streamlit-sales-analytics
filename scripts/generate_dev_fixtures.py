"""Generate deterministic Parquet fixtures for local SQLite dev mode."""

from pathlib import Path

from streamlit_app.dev_fixtures import write_parquet_fixtures


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_dir = repo_root / "fixtures" / "sales_seed"
    write_parquet_fixtures(fixture_dir)
    print(f"Wrote local dev fixtures to {fixture_dir}")


if __name__ == "__main__":
    main()
