# Economic Insights Dashboard

This project is a Streamlit dashboard for visualizing key economic indicators from the World Bank.

## How to Run

1.  **Set up the environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```

2.  **Fetch the data:**

    This script downloads the required economic indicators from the World Bank API and saves them locally as raw and processed CSV files.

    ```bash
    python src/fetch_worldbank.py
    ```

    **Outputs:**
    - `data/raw/worldbank_raw.csv`
    - `data/processed.csv`

## Data Transformation Layer

The `src/transform.py` module is responsible for cleaning, standardizing, and enriching the processed data to make it suitable for analysis and visualization. It acts as a bridge between the raw, processed data and the final application.

Key transformations include:
- **Forward Filling:** Missing data points for each country are filled using the last known value for that specific country, preventing data leakage across different nations.
- **Z-Score Standardization:** Key economic indicators are normalized on a per-country basis. This allows for comparing a data point to its historical average for that country.
- **Feature Engineering:** New, insightful metrics such as the "Misery Index" (Unemployment + Inflation) and "Debt-to-Growth Ratio" are created to provide deeper economic insights.

### Running with Docker

To run the application using Docker, ensuring a consistent development environment:

1.  **Build the Docker image and start the containers:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image (if not already built) and start the data fetcher and the Streamlit application in separate containers.

2.  **Access the application:**
    The application will be available at `http://localhost:8501`.

**Note:** If port 8501 is in use locally, you may need to adjust the port mapping in the `docker-compose.yml` file.

---

### CI Status

[![CI Status](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/ci.yml)
### Enhanced Visualizations and Dashboard Layout

This update significantly enhances the dashboard's analytical capabilities by introducing a more interactive user interface and advanced visualization tools.

*   **Tabbed Interface:** The main dashboard area has been reorganized into two distinct tabs:
    *   **Time Series Explorer:** Displays the existing time-series comparison charts, allowing users to select multiple countries and a metric for analysis.
    *   **Metric Relationships:** This new tab provides tools for in-depth exploratory data analysis. Users can select a single country and then choose two metrics to visualize their relationship:
        *   **Correlation Heatmap:** Visualizes the correlation matrix of key economic indicators for the selected country, helping to identify relationships between different metrics.
        *   **Scatter Plot:** Allows users to plot any two selected metrics against each other for the chosen country, revealing patterns and correlations.


## Running the Application

To launch the interactive Streamlit dashboard:

```bash
streamlit run app.py
```

This will open the application in your web browser, allowing you to explore the economic data with interactive controls.