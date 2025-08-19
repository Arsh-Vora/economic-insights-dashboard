import os
import requests
import pandas as pd
import sys
from time import sleep


COUNTRIES = ["IT", "US", "IN", "BR", "CN", "ZA", "DE"]
INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "FP.CPI.TOTL.ZG": "inflation_cpi",
    "SL.UEM.TOTL.ZS": "unemployment_rate",
    "GC.DOD.TOTL.GD.ZS": "gov_debt_pct_gdp",
    "BN.CAB.XOKA.GD.ZS": "current_account_pct_gdp",
}
START_YEAR, END_YEAR = 2000, 2024
BASE_URL = "http://api.worldbank.org/v2/country"
DATA_DIR = "data"
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "worldbank_raw.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed.csv")


def fetch_indicator(country_code: str, indicator: str) -> pd.DataFrame:
    """
    Fetches a single indicator for a single country from the World Bank API.

    Args:
        country_code: The ISO3 code of the country.
        indicator: The World Bank indicator code.

    Returns:
        A DataFrame with the requested data, or None if the request fails or returns no data.
    """
    url = f"{BASE_URL}/{country_code}/indicator/{indicator}"
    params = {
        "format": "json",
        "date": f"{START_YEAR}:{END_YEAR}",
        "per_page": "1000",  
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not fetch data for {country_code}/{indicator}. Reason: {e}", file=sys.stderr)
        return None

    data = response.json()

   
    if not data or len(data) < 2 or not isinstance(data[1], list) or not data[1]:
        print(f"  -> Skipping for {country_code}/{indicator} due to empty or invalid API response.")
        return None

    df = pd.json_normalize(data[1])

    required_cols = {'country.value', 'countryiso3code', 'date', 'value', 'indicator.id'}
    if not required_cols.issubset(df.columns):
        print(f"  -> Skipping for {country_code}/{indicator} due to missing columns in API response.", file=sys.stderr)
        return None
    
    df = df[list(required_cols)]
    df.rename(columns={'indicator.id': 'indicator'}, inplace=True)
    
    return df


def main():
    """
    Main function to orchestrate the data fetching and processing pipeline.
    - Fetches data for all configured countries and indicators.
    - Persists the combined raw data to a CSV file.
    - Processes the raw data into a wide format.
    - Persists the processed data to a CSV file.
    """
    print("Starting World Bank data fetch...")
    
    os.makedirs(os.path.join(DATA_DIR, "raw"), exist_ok=True)
    
    all_dataframes = []
    total_requests = len(COUNTRIES) * len(INDICATORS)
    request_count = 0

    for country in COUNTRIES:
        for indicator_code in INDICATORS.keys():
            request_count += 1
            print(f"({request_count}/{total_requests}) Fetching {indicator_code} for {country}...")
            
            df = fetch_indicator(country, indicator_code)
            
            if df is not None and not df.empty and df['value'].notna().any():
                all_dataframes.append(df)
            else:
                print(f"  -> Skipping empty or all-NA data for {country}/{indicator_code}")

            sleep(0.1)

    if not all_dataframes:
        print("ERROR: No data fetched. Exiting.", file=sys.stderr)
        sys.exit(1)

    print("\nConcatenating and saving raw data...")
    raw_df = pd.concat(all_dataframes, ignore_index=True)
    
    raw_df['date'] = pd.to_numeric(raw_df['date'])
    raw_df['value'] = pd.to_numeric(raw_df['value'], errors='coerce')
    
    raw_df.sort_values(by=["countryiso3code", "date"], inplace=True)
    raw_df.to_csv(RAW_DATA_PATH, index=False)
    print(f"-> Raw data saved to {RAW_DATA_PATH} ({len(raw_df)} rows)")

    print("\nPivoting and saving processed data...")
    
    processed_df = raw_df.copy()
    processed_df['indicator'] = processed_df['indicator'].map(INDICATORS)
    
    processed_df = processed_df.pivot_table(
        index=['country.value', 'countryiso3code', 'date'],
        columns='indicator',
        values='value',
        aggfunc='mean'
    ).reset_index()

    processed_df.sort_values(by=["countryiso3code", "date"], inplace=True)
    processed_df.rename_axis(None, axis=1, inplace=True)
    
    processed_df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"-> Processed data saved to {PROCESSED_DATA_PATH} ({len(processed_df)} rows)")

    print("\nPipeline finished successfully.")


if __name__ == "__main__":
    main()