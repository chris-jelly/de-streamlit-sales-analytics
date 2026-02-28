## Purpose
Define the baseline native Streamlit theming contract for the dashboard, including repository-managed visual tokens and a no-CSS-overrides policy for core theme concerns.

## Requirements

### Requirement: Dashboard defines a native Streamlit theme baseline
The dashboard SHALL define a repository-managed native Streamlit theme in `.streamlit/config.toml` for core visual tokens.

#### Scenario: Theme config exists with core tokens
- **WHEN** repository configuration is reviewed
- **THEN** `.streamlit/config.toml` SHALL define `[theme]` values for primary color, background color, secondary background color, text color, and typography

#### Scenario: Sidebar and chart presentation are explicitly themed
- **WHEN** the dashboard UI is rendered
- **THEN** sidebar styling and chart palette tokens SHALL be configured through Streamlit theme settings rather than implicit defaults

### Requirement: Theming uses native Streamlit configuration rather than CSS overrides
The system SHALL use Streamlit theme configuration as the source of truth for application theming.

#### Scenario: No custom CSS for core theming concerns
- **WHEN** app code is reviewed for theme behavior
- **THEN** colors, typography, and global surfaces SHALL be controlled via `.streamlit/config.toml` and SHALL NOT depend on injected CSS or HTML style blocks
