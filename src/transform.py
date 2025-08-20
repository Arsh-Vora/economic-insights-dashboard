import pandas as pd
import numpy as np

PROCESSED_DATA_PATH = "data/processed.csv"

def load_processed_data() -> pd.DataFrame:
    """Loads the processed data from the CSV file."""
    df = pd.read_csv(PROCESSED_DATA_PATH, dtype={'date': str})
    df['date'] = pd.to_datetime(df['date'], format='%Y')
    return df

def forward_fill_per_country(df: pd.DataFrame, metrics: list) -> pd.DataFrame:
    """
    Applies forward-fill to specified metrics, grouped by country.
    This prevents data leakage between countries.
    """
    df_copy = df.copy()
    for metric in metrics:
        df_copy[metric] = df_copy.groupby('countryiso3code')[metric].transform(lambda x: x.ffill())
    return df_copy

def standardize_features(df: pd.DataFrame, metrics: list) -> pd.DataFrame:
    """
    Calculates the Z-score for the given metrics on a per-country basis.
    This normalizes each metric to its historical mean and standard deviation for a given country.
    """
    df_copy = df.copy()
    for metric in metrics:
        group_transform = df_copy.groupby('countryiso3code')[metric].transform(
            lambda x: np.where(x.std() != 0, (x - x.mean()) / x.std(), np.nan)
        )
        df_copy[f"{metric}_z"] = group_transform
    return df_copy

def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds new composite features to the DataFrame.
    - Misery Index
    - Debt to Growth Ratio
    - External Balance Health (alias)
    """
    df_copy = df.copy()
    df_copy['misery_index'] = df_copy['unemployment_rate'] + df_copy['inflation_cpi']
    df_copy['debt_to_growth_ratio'] = np.where(df_copy['gdp_growth'] != 0, df_copy['gov_debt_pct_gdp'] / df_copy['gdp_growth'], np.nan)
    df_copy['current_account_balance'] = df_copy['current_account_pct_gdp']
    
    return df_copy

def validate_schema(df: pd.DataFrame, required_cols: list):
    """
    Validates that the input DataFrame contains all required columns.
    Raises a KeyError if any columns are missing.
    """
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"The following required columns are missing from the DataFrame: {missing_cols}")

def build_dataset() -> pd.DataFrame:
    """
    Orchestrates the full transformation pipeline:
    1. Loads data.
    2. Validates schema.
    3. Forward-fills missing values.
    4. Standardizes key metrics.
    5. Adds engineered features.
    
    Returns:
        The fully transformed and enriched DataFrame.
    """
    METRICS_TO_TRANSFORM = [
        'gdp_growth', 'inflation_cpi', 'unemployment_rate',
        'gov_debt_pct_gdp', 'current_account_pct_gdp'
    ]
    
    df = load_processed_data()

    validate_schema(df, METRICS_TO_TRANSFORM + ['countryiso3code'])
    df = forward_fill_per_country(df, METRICS_TO_TRANSFORM)
    df = standardize_features(df, METRICS_TO_TRANSFORM)
    df = add_engineered_features(df)
    
    print("Transformation pipeline complete. Enriched DataFrame is ready.")
    return df

if __name__ == '__main__':
    enriched_df = build_dataset()
    print("\n--- Enriched DataFrame ---")
    print(enriched_df.head())
    print("\nColumns:", enriched_df.columns.tolist())
    print(f"\nShape: {enriched_df.shape}")