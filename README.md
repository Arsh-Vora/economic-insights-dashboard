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