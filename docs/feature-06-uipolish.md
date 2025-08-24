## Feature 06 — Documentation & UI Polish

### 1. Goal

Improve the overall user experience and professional appearance of the dashboard by adding in-app documentation, contextual information about the metrics, and refining the user interface layout. This will make the application more intuitive and valuable for end-users who may not be familiar with all the economic indicators.

### 2. Deliverables

*   `app.py`: **Updated** with a refined layout, titles, introductory text, and dynamic metric descriptions.
*   `src/config.py`: A **new** file to store configuration data, such as metric definitions, to decouple content from the application logic.
*   `docs/feature-06-ui-polish.md`: This implementation plan.
*   `README.md`: **Updated** with a more descriptive summary of the application's features.

---

### 3. Scope

#### In

*   **Centralized Metric Configuration:** Create a `src/config.py` file to store a list or dictionary of all plottable metrics. Each entry will contain:
    *   The column ID (e.g., `gdp_growth`).
    *   A user-friendly display name (e.g., "GDP Growth Rate (%)").
    *   A clear description of the metric.
*   **App Header:** Add a main title (`st.title`) and a brief introductory paragraph (`st.markdown`) at the top of the application to explain its purpose.
*   **Dynamic Metric Descriptions:** In all tabs, whenever a user selects a metric from a dropdown (for the time-series or scatter plots), its description will be displayed directly below the selector using `st.info` or `st.markdown`.
*   **User-Friendly Selectors:** The metric selection dropdowns will now display the friendly names (e.g., "Misery Index") instead of the raw column names (e.g., `misery_index`).
*   **"About" Tab:** Add a third tab to the main interface named "About". This tab will contain:
    *   Information about the data source (World Bank World Development Indicators).
    *   A brief explanation of the engineered features.
    *   The purpose of the dashboard.
*   **Layout Refinements:** Minor adjustments like adding dividers (`st.divider`) to visually separate sections and improving chart titles for clarity.

#### Out

*   Fetching new data or changing the data transformation logic.
*   Adding any new plots or analytical features.
*   Implementing custom CSS for styling. All improvements will use native Streamlit components.
*   User account management or personalization features.

---

### 4. Architecture

The architecture is enhanced by introducing a configuration module (`config.py`). This improves maintainability by separating the UI's content and definitions from its structural logic in `app.py`, following the principle of Separation of Concerns.

```mermaid
flowchart TD
    subgraph "Configuration"
        A[src/config.py]
        A -- Defines --> B(Metric Definitions<br/>- ID<br/>- Display Name<br/>- Description)
    end

    subgraph "Streamlit Application"
        C[app.py]
    end
    
    subgraph "UI Components"
        D[st.selectbox "Metric"]
        E[st.info "Metric Description"]
        F[st.tabs]
    end

    A -- Imported by --> C
    C -- Uses Config to Populate --> D
    D -- User Selects Metric --> C
    C -- Uses Config to Find & Display --> E
    C -- Manages Layout --> F
```

---

### 5. Implementation Details / Technical Approach

*   **`src/config.py`:**
    *   Create a list of dictionaries to define the metrics. This structure is easy to iterate over and access.
    ```python
    # src/config.py
    METRICS_CONFIG = [
        {
            "id": "gdp_growth",
            "display_name": "GDP Growth Rate (%)",
            "description": "The annual percentage growth rate of Gross Domestic Product (GDP)..."
        },
        {
            "id": "misery_index",
            "display_name": "Misery Index",
            "description": "A simple economic indicator calculated by adding the unemployment rate to the inflation rate."
        },
        # ... add all other metrics (raw, _z, and engineered)
    ]
    ```

*   **`app.py`:**
    *   At the top, add `import src.config as config` and `st.title(...)`, `st.markdown(...)`.
    *   **Refactor `st.selectbox`:**
        *   To populate the dropdown, use a list of the metric IDs: `metric_ids = [m['id'] for m in config.METRICS_CONFIG]`.
        *   To display the friendly names, use the `format_func` argument:
            ```python
            # Create a mapping from ID to display name for quick lookup
            metric_display_map = {m['id']: m['display_name'] for m in config.METRICS_CONFIG}

            selected_metric_id = st.selectbox(
                label="Select Metric:",
                options=metric_ids,
                format_func=lambda id: metric_display_map.get(id, id)
            )
            ```
    *   **Display Descriptions:**
        *   After getting the `selected_metric_id`, find the full metric object and display its description.
            ```python
            # Find the full config for the selected metric
            selected_metric_config = next((m for m in config.METRICS_CONFIG if m['id'] == selected_metric_id), None)

            if selected_metric_config:
                st.info(selected_metric_config['description'])
            ```
        *   Apply this logic under every metric selector in the application.
    *   **"About" Tab:**
        *   Change the tab creation to: `tab1, tab2, tab3 = st.tabs([... , "About"])`.
        *   In the `with tab3:` block, add text content using `st.header` and `st.markdown`.

---

### 6. Definition of Done

*   [ ] A `src/config.py` file is created and populated with definitions for all metrics.
*   [ ] The application displays a main title and an introduction.
*   [ ] All metric selection dropdowns show user-friendly names instead of column IDs.
*   [ ] A description for the selected metric is displayed below each dropdown.
*   [ ] A new "About" tab exists and contains relevant project and data source information.
*   [ ] Minor layout improvements (e.g., dividers) have been added for clarity.
*   [ ] The application is fully functional and runs without errors.
*   [ ] A PR is opened to `dev` from `feature/ui-polish`.

---

### 7. File Manifest

Files created or modified in this feature:

```
src/config.py
app.py
docs/feature-06-ui-polish.md
README.md
```

---

### 8. Conventional Commits

*   `feat(config): create centralized configuration for metric definitions`
*   `feat(ui): display dynamic metric descriptions based on user selection`
*   `refactor(ui): use friendly names in metric dropdowns`
*   `feat(ui): add 'About' tab with project and data source details`
*   `style(ui): add title, intro, and dividers for better layout`

---

### 9. Pull Request Template

**Title:** `feat: improve usability with in-app documentation and UI polish`

**Summary:**
This PR focuses on enhancing the user experience of the dashboard. Instead of adding new analytical features, it makes the existing ones more understandable and professional.

Key Changes:
1.  **Metric Configuration (`src/config.py`):** All metric definitions (display names, descriptions) are now managed in a central configuration file, decoupling content from logic.
2.  **Dynamic Descriptions:** The app now displays a clear description of any metric the user selects in a dropdown, providing immediate context.
3.  **Improved UI/UX:** Metric selectors now show human-readable names, and a new "About" tab provides high-level information about the project and its data source.
4.  **Polished Layout:** A main title, introduction, and visual separators have been added to create a more polished and professional look.

**Checklist:**
*   [ ] `src/config.py` has been created and populated.
*   [ ] All metric selectors have been updated to be more user-friendly.
*   [ ] The new "About" tab is present and contains correct information.
*   [ ] The overall application layout is improved and looks polished.
*   [ ] The code adheres to project styling and quality standards.