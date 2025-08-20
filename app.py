import streamlit as st
import sys
import os

# Add project root to sys.path to ensure local imports work
# This helps Python find the 'src' directory when running scripts from different contexts.
sys.path.append(os.path.dirname(__file__))
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
all_countries = sorted(df['country.value'].unique().tolist() if not df.empty else [])
default_countries = os.environ.get("DEFAULT_COUNTRIES", "United States,China,Germany").split(",")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=all_countries,
    default=[country.strip() for country in default_countries if country.strip() in all_countries]
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
# Introduce tabs
tab1, tab2 = st.tabs(["Time Series Explorer", "Metric Relationships"])

# Tab 1: Time Series Explorer
with tab1:
    st.title(f"{selected_metric_display_name} Comparison")

    if not selected_countries:
        st.info("Please select at least one country to display the chart.")
    else:
        # Filter data based on selections
        filtered_df = df[df['country.value'].isin(selected_countries)]

        # Generate and display plot
        plot_title = f"{selected_metric_display_name} for Selected Countries"
        fig = plots.generate_time_series_plot(filtered_df, selected_metric_column_name, plot_title)
        if fig is None or len(fig.data) == 0:
            st.info("No data available for the selected criteria.")
        else:
            st.plotly_chart(fig, use_container_width=True)

        # Data Preview Expander
        with st.expander("▼ Show Plotted Data"):
            st.dataframe(filtered_df[['date', 'country.value', selected_metric_column_name]].sort_values(by=['country.value', 'date']))

# Tab 2: Metric Relationships
with tab2:
    st.title("Metric Relationships")

    # Country Selector for Relationships Tab
    # Use the same country list as the sidebar, but make it a single select
    # Ensure a default country is selected if available
    default_country_for_relationships = selected_countries[0] if selected_countries else (all_countries[0] if all_countries else None)
    
    country_for_relationships = st.selectbox(
        "Select a Country:",
        options=all_countries,
        index=all_countries.index(default_country_for_relationships) if default_country_for_relationships in all_countries else 0,
        key="relationships_country_select" # Add a unique key
    )

    if country_for_relationships:
        country_df = df[df['country.value'] == country_for_relationships]

        # Correlation Heatmap
        st.header("Correlation Heatmap")
        # Define metrics to correlate, using the keys from plottable_metrics
        metrics_to_correlate = list(plottable_metrics.values())
        
        # Check if country_df is not empty and has the metrics
        if not country_df.empty and all(metric in country_df.columns for metric in metrics_to_correlate):
            corr_fig = plots.generate_correlation_heatmap(country_df, metrics_to_correlate)
            if corr_fig is not None:
                st.plotly_chart(corr_fig, use_container_width=True)
            else:
                st.info("No data available for correlation heatmap for the selected country.")
        else:
            st.info("No data available for correlation heatmap for the selected country.")

        st.markdown("---")

        # Scatter Plot
        st.header("Scatter Plot Explorer")
        
        # X-Axis Metric Selector
        x_metric_display_name = st.selectbox(
            "Select X-Axis Metric:",
            options=list(plottable_metrics.keys()),
            index=0, # Default to GDP Growth
            key="scatter_x_metric_select" # Add a unique key
        )
        x_metric_column_name = plottable_metrics[x_metric_display_name]

        # Y-Axis Metric Selector
        y_metric_display_name = st.selectbox(
            "Select Y-Axis Metric:",
            options=list(plottable_metrics.keys()),
            index=1, # Default to Inflation (CPI)
            key="scatter_y_metric_select" # Add a unique key
        )
        y_metric_column_name = plottable_metrics[y_metric_display_name]

        # Generate and display scatter plot
        if not country_df.empty and x_metric_column_name in country_df.columns and y_metric_column_name in country_df.columns:
            scatter_fig = plots.generate_scatter_plot(country_df, x_metric_column_name, y_metric_column_name)
            if scatter_fig is not None:
                st.plotly_chart(scatter_fig, use_container_width=True)
            else:
                st.info("No data available for scatter plot for the selected criteria.")
        else:
            st.info("No data available for scatter plot for the selected criteria.")

st.markdown("---")
st.caption("Data Source: World Bank Indicators")