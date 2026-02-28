## 1. View orchestration refactor

- [x] 1.1 Replace `st.tabs`-based top-level navigation with a single active-view selector that targets `Overview`, `Forecast`, and `History`
- [x] 1.2 Update app render flow so only the selected heavy view renderer executes per rerun while preserving existing freshness behavior per view
- [x] 1.3 Validate that global filters still apply consistently across all three views after orchestration changes

## 2. Theme baseline setup

- [x] 2.1 Add `.streamlit/config.toml` with required `[theme]` tokens for primary/background/secondary/text colors and typography
- [x] 2.2 Configure sidebar and chart palette theme values to avoid reliance on Streamlit defaults
- [x] 2.3 Confirm app code does not use CSS/HTML-based theming overrides for global colors, fonts, or surfaces

## 3. Dashboard layout standardization

- [x] 3.1 Update KPI and section composition to use consistent dashboard card/grouping patterns aligned with the new design baseline
- [x] 3.2 Ensure sidebar remains scoped to global filters and app-level metadata only
- [x] 3.3 Keep existing Phase 1 content scope intact for `Overview`, `Forecast`, and `History` while applying layout conventions

## 4. Verification and documentation

- [x] 4.1 Add or update tests/checks to verify active-view execution semantics and unchanged KPI/filter contracts
- [x] 4.2 Run repository test suite and resolve regressions introduced by the refactor
- [x] 4.3 Update `README.md` and/or runtime docs with the new view orchestration and theming conventions
