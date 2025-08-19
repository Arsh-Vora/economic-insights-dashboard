# Data Dictionary

This document provides a definition for all columns present in the final, enriched dataset produced by the `src/transform.py` module.

## Core Metrics (Raw & Processed)

These are the primary indicators fetched from the World Bank.

| Column | Type | Description |
|---|---|---|
| `country.value` | string | The full name of the country. |
| `countryiso3code` | string | The 3-letter ISO code for the country. |
| `date` | integer | The year of the observation. |
| `gdp_growth` | float | Annual GDP growth rate (%). |
| `inflation_cpi` | float | Annual inflation rate based on the Consumer Price Index (%). |
| `unemployment_rate` | float | The percentage of the labor force that is without jobs. |
| `gov_debt_pct_gdp` | float | General government gross debt as a percentage of GDP. |
| `current_account_pct_gdp` | float | Current account balance as a percentage of GDP. |

## Standardized Metrics (Z-Scores)

These columns represent the Z-score for each core metric, calculated on a per-country basis. A Z-score indicates how many standard deviations an observation is from its country's historical mean.

| Column | Type | Description |
|---|---|---|
| `gdp_growth_z` | float | Z-score of `gdp_growth`. |
| `inflation_cpi_z`| float | Z-score of `inflation_cpi`. |
| `unemployment_rate_z`| float | Z-score of `unemployment_rate`. |
| `gov_debt_pct_gdp_z`| float | Z-score of `gov_debt_pct_gdp`. |
| `current_account_pct_gdp_z`| float | Z-score of `current_account_pct_gdp`. |

## Engineered Features

These columns are composite indicators created from the core metrics to provide additional insights.

| Column | Type | Description |
|---|---|---|
| `misery_index` | float | A simple economic indicator calculated as `unemployment_rate + inflation_cpi`. |
| `debt_to_growth_ratio` | float | The ratio of government debt to GDP growth (`gov_debt_pct_gdp / gdp_growth`). |
| `external_balance_health`| float | An alias for `current_account_pct_gdp`, representing the health of a country's trade balance. |