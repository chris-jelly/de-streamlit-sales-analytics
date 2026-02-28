## Why

The current Streamlit dashboard has a strong data and module foundation, but it diverges from several recently added Streamlit best-practice guidelines around execution flow, theming, and dashboard composition. Aligning now reduces performance risk as data volume grows and creates a clearer UX baseline for future phases.

## What Changes

- Replace tab-driven heavy rendering with conditional view selection so expensive sections only compute when selected.
- Introduce native Streamlit theme configuration in `.streamlit/config.toml` and define a consistent visual system for typography, color, and component surfaces.
- Standardize dashboard layout patterns (KPI cards, bordered groupings, sidebar/global filter boundaries) to improve readability and consistency.
- Remove Streamlit entry-point patterns that conflict with current guidance (e.g., main guard in the app script) and codify the preferred app structure.
- Add lightweight guardrails and verification criteria so future UI/performance changes follow the same conventions.

## Capabilities

### New Capabilities
- `streamlit-theming-baseline`: Define and enforce a native Streamlit theme baseline (no CSS-based theming) for the dashboard app.

### Modified Capabilities
- `streamlit-phase1-dashboard`: Update dashboard runtime and presentation requirements to use conditional rendering patterns instead of always-rendered heavy tab content, and to apply standardized layout conventions.

## Impact

- Affected code: `streamlit_app/app.py`, `streamlit_app/tabs.py`, and potentially `streamlit_app/filters.py` for interaction and layout behavior.
- New configuration surface: `.streamlit/config.toml` for theme tokens and visual defaults.
- Documentation updates in `README.md` and/or `docs/` to reflect UI/performance conventions.
- No external API contract changes; internal dashboard behavior and maintainability improve.
