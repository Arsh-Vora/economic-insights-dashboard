import streamlit as st
import src.transform as transform
import src.plots as plots
import pandas as pd
import os

# Set page config
st.set_page_config(
    page_title="Economic Insights Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """
    Loads and caches the transformed economic dataset.
    """
    try:
        df = transform.build_dataset()
        # Ensure 'date' column is datetime and set as index for easier filtering
        # Date conversion is now handled in src.transform.build_dataset
        return df
    except FileNotFoundError:
        st.error("Error: Data file 'data/processed.csv' not found. Please ensure Feature 2 (data transformation) has been run.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        st.stop()

# Load data
df = load_data()

# --- Sidebar Controls ---
st.sidebar.title("📈 Economic Dashboard")
st.sidebar.markdown("---")
st.sidebar.header("**Controls**")

# Country Multi-select
all_countries = sorted(df['country.value'].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=all_countries,
    default=["United States", "China", "Germany"] # Default selection
)

# Metric Select Box
plottable_metrics = {
    "GDP Growth": 'gdp_growth',
    "Inflation (CPI)": 'inflation_cpi_z',
    "Misery Index": 'misery_index',
    "Unemployment Rate": 'unemployment_rate',
    "Current Account Balance": 'current_account_balance'
} # Define your plottable metrics here

selected_metric_display_name = st.sidebar.selectbox(
    "Select Metric:",
    options=list(plottable_metrics.keys()),
    index=0 # Default to the first metric
)
selected_metric_column_name = plottable_metrics[selected_metric_display_name]

# --- Main Panel ---
st.title(f"{selected_metric_display_name} Comparison")

if not selected_countries:
    st.info("Please select at least one country to display the chart.")
else:
    # Filter data based on selections
    filtered_df = df[df['country.value'].isin(selected_countries)]

    # Generate and display plot
    plot_title = f"{selected_metric_display_name} for Selected Countries"
    fig = plots.generate_time_series_plot(filtered_df, selected_metric_column_name, plot_title)
    st.plotly_chart(fig, use_container_width=True)

    # Data Preview Expander
    with st.expander("▼ Show Plotted Data"):
        st.dataframe(filtered_df[['date', 'country.value', selected_metric_column_name]].sort_values(by=['country.value', 'date']))

st.markdown("---")
st.caption("Data Source: World Bank Indicators")