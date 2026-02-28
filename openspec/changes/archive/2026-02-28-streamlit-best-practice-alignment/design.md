## Context

The current Phase 1 dashboard already separates data access, filter logic, and tab renderers, and uses Streamlit caching for the warehouse client and data fetches. However, its view composition still relies on `st.tabs`, which evaluates all tab content on each rerun. As data volume and chart complexity increase, this creates avoidable compute and latency. The app also lacks a repository-native Streamlit theme baseline, making visual consistency and future design evolution ad hoc.

Stakeholders are internal analytics consumers and maintainers of the `streamlit_app` package. Constraints include preserving existing KPI semantics, canonical mart usage, and current global filter behavior.

## Goals / Non-Goals

**Goals:**
- Shift dashboard view orchestration to a conditional-rendering pattern where heavy visual sections compute only for the actively selected view.
- Establish a first-class native Streamlit theme baseline in `.streamlit/config.toml` (no CSS theming dependency).
- Standardize dashboard composition patterns (KPI cards, bordered groups, sidebar role) so future additions follow a predictable structure.
- Keep business metrics and source-model contracts unchanged while improving runtime behavior and maintainability.

**Non-Goals:**
- Redefining KPI formulas or changing canonical source marts.
- Introducing multipage navigation, authentication, or new analytics domains.
- Building custom Streamlit components or front-end frameworks.

## Decisions

### 1) Replace tab-first rendering with explicit active-view control
- Decision: Use a single active-view selector (for example segmented control or radio) and render exactly one heavy content branch per rerun.
- Rationale: Streamlit tabs render all branches; explicit branching avoids unnecessary chart/table computation.
- Alternatives considered:
  - Keep `st.tabs` and rely on caching only: rejected because hidden tab compute still occurs.
  - Split each view into a separate page: deferred; multipage is unnecessary for current scope.

### 2) Keep existing cache architecture, tighten execution boundaries
- Decision: Retain `@st.cache_resource` for the warehouse client and `@st.cache_data(ttl=...)` for date-window datasets, while moving expensive transforms behind active-view conditionals.
- Rationale: Existing cache approach is sound; the main issue is unconditional rendering.
- Alternatives considered:
  - Aggressive per-chart caching: not required initially; increases key management complexity.
  - Fragment-based live updates: not needed for current non-live dashboard behavior.

### 3) Adopt native theme configuration as the only theming mechanism
- Decision: Add `.streamlit/config.toml` with explicit color, typography, border, and chart palette tokens.
- Rationale: Native theming is durable across Streamlit upgrades and avoids brittle CSS selectors.
- Alternatives considered:
  - Custom CSS with `unsafe_allow_html=True`: rejected for maintainability and compatibility reasons.
  - No theme baseline: rejected because UI consistency remains undefined.

### 4) Encode layout conventions in app composition
- Decision: Require KPI card presentation and consistent grouping/container usage for overview and analytical sections.
- Rationale: Improves readability and lowers cognitive load when new views are added.
- Alternatives considered:
  - Allow ad hoc layout per view: rejected because it fragments UX over time.

## Risks / Trade-offs

- [Risk] Active-view control change may alter user interaction expectations for those accustomed to tabs. -> Mitigation: keep the three named views (`Overview`, `Forecast`, `History`) and preserve visible freshness + filter behavior.
- [Risk] Theme token choices may reduce readability if contrast is poorly tuned. -> Mitigation: require contrast checks for text, primary buttons, sidebar, and dataframe headers during verification.
- [Risk] Conditional rendering can accidentally skip shared computations needed by multiple views. -> Mitigation: isolate shared pre-processing in common functions and test each view path independently.
- [Trade-off] Standardized layout limits stylistic flexibility. -> Mitigation: prioritize consistency now; evolve design language intentionally through future spec updates.

## Migration Plan

1. Add and validate theme baseline config in `.streamlit/config.toml`.
2. Refactor app view orchestration to single-active-view conditional rendering while preserving existing view names and outputs.
3. Apply standardized card/layout patterns across view renderers.
4. Run existing tests and add targeted checks for active-view execution behavior.
5. Update docs to encode the new composition and theming conventions.

Rollback strategy: revert to prior app orchestration and remove theme config if UX/performance regressions are observed.

## Open Questions

- Which selector control best fits expected user behavior (`st.segmented_control` vs `st.radio`) for view switching?
- Should the first release of this change include a lightweight lint/checklist for Streamlit conventions, or only documentation + code patterns?
