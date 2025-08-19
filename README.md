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