# src/config.py
METRICS_CONFIG = [
    {
        "id": "gdp_growth",
        "display_name": "GDP Growth Rate (%)",
        "description": "The annual percentage growth rate of Gross Domestic Product (GDP)..."
    },
    {
        "id": "inflation_cpi",
        "display_name": "Inflation Rate (CPI, %)",
        "description": "Annual inflation rate based on the Consumer Price Index (%)."
    },
    {
        "id": "unemployment_rate",
        "display_name": "Unemployment Rate (%)",
        "description": "The percentage of the labor force that is without jobs."
    },
    {
        "id": "gov_debt_pct_gdp",
        "display_name": "Government Debt (% of GDP)",
        "description": "General government gross debt as a percentage of GDP."
    },
    {
        "id": "current_account_pct_gdp",
        "display_name": "Current Account Balance (% of GDP)",
        "description": "Current account balance as a percentage of GDP."
    },
    {
        "id": "misery_index",
        "display_name": "Misery Index",
        "description": "A simple economic indicator calculated as unemployment_rate + inflation_cpi."
    },
    {
        "id": "debt_to_growth_ratio",
        "display_name": "Debt to Growth Ratio",
        "description": "The ratio of government debt to GDP growth (gov_debt_pct_gdp / gdp_growth)."
    },
    {
        "id": "external_balance_health",
        "display_name": "External Balance Health",
        "description": "An alias for current_account_pct_gdp, representing the health of a country's trade balance."
    },
    {
        "id": "gdp_growth_z",
        "display_name": "GDP Growth Rate (Z-score)",
        "description": "Z-score of gdp_growth."
    },
    {
        "id": "inflation_cpi_z",
        "display_name": "Inflation Rate (CPI, Z-score)",
        "description": "Z-score of inflation_cpi."
    },
    {
        "id": "unemployment_rate_z",
        "display_name": "Unemployment Rate (Z-score)",
        "description": "Z-score of unemployment_rate."
    },
    {
        "id": "gov_debt_pct_gdp_z",
        "display_name": "Government Debt (Z-score)",
        "description": "Z-score of gov_debt_pct_gdp."
    },
    {
        "id": "current_account_pct_gdp_z",
        "display_name": "Current Account Balance (Z-score)",
        "description": "Z-score of current_account_pct_gdp."
    }
]