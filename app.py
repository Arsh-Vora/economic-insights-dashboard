import streamlit as st
import sys
import os



sys.path.append(os.path.dirname(__file__))
import src.transform as transform
import src.plots as plots
import os


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
        
        
        return df
    except FileNotFoundError:
        st.error("Error: Data file 'data/processed.csv' not found. Please ensure Feature 2 (data transformation) has been run.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while loading data: {e}")
        st.stop()


df = load_data()


st.sidebar.title("📈 Economic Dashboard")
st.sidebar.markdown("---")
st.sidebar.header("**Controls**")


all_countries = sorted(df['country.value'].unique().tolist() if not df.empty else [])
default_countries = os.environ.get("DEFAULT_COUNTRIES", "United States,China,Germany").split(",")
selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=all_countries,
    default=[country.strip() for country in default_countries if country.strip() in all_countries]
)


plottable_metrics = {
    "GDP Growth": 'gdp_growth',
    "Inflation (CPI)": 'inflation_cpi_z',
    "Misery Index": 'misery_index',
    "Unemployment Rate": 'unemployment_rate',
    "Current Account Balance": 'current_account_balance'
} 

selected_metric_display_name = st.sidebar.selectbox(
    "Select Metric:",
    options=list(plottable_metrics.keys()),
    index=0 
)
selected_metric_column_name = plottable_metrics[selected_metric_display_name]



tab1, tab2 = st.tabs(["Time Series Explorer", "Metric Relationships"])


with tab1:
    st.title(f"{selected_metric_display_name} Comparison")

    if not selected_countries:
        st.info("Please select at least one country to display the chart.")
    else:
        
        filtered_df = df[df['country.value'].isin(selected_countries)]

        
        plot_title = f"{selected_metric_display_name} for Selected Countries"
        fig = plots.generate_time_series_plot(filtered_df, selected_metric_column_name, plot_title)
        if fig is None or len(fig.data) == 0:
            st.info("No data available for the selected criteria.")
        else:
            st.plotly_chart(fig, use_container_width=True)

        
        with st.expander("▼ Show Plotted Data"):
            st.dataframe(filtered_df[['date', 'country.value', selected_metric_column_name]].sort_values(by=['country.value', 'date']))


with tab2:
    st.title("Metric Relationships")

    
    
    
    country_for_relationships = st.selectbox(
        "Select a Country:",
        options=all_countries,
        index=all_countries.index(selected_countries[0]) if selected_countries else 0,
        key="relationships_country_select"
    )

    if country_for_relationships:
        country_df = df[df['country.value'] == country_for_relationships]

        
        st.header("Correlation Heatmap")
        metrics_to_correlate = list(plottable_metrics.values())
        if not country_df.empty and all(metric in country_df.columns for metric in metrics_to_correlate):
            corr_fig = plots.generate_correlation_heatmap(country_df, metrics_to_correlate)
            st.plotly_chart(corr_fig, use_container_width=True) if corr_fig else st.info("No data available for correlation heatmap for the selected country.")
        else:
            st.info("No data available for correlation heatmap for the selected country.")

        st.markdown("---")

        
        st.header("Scatter Plot Explorer")
        
        
        x_metric_display_name = st.selectbox(
            "Select X-Axis Metric:",
            options=list(plottable_metrics.keys()),
            index=0, 
            key="scatter_x_metric_select" 
        )
        x_metric_column_name = plottable_metrics[x_metric_display_name]

        
        y_metric_display_name = st.selectbox(
            "Select Y-Axis Metric:",
            options=list(plottable_metrics.keys()),
            index=1, 
            key="scatter_y_metric_select" 
        )
        y_metric_column_name = plottable_metrics[y_metric_display_name]

        
        if not country_df.empty and x_metric_column_name in country_df.columns and y_metric_column_name in country_df.columns:
            scatter_fig = plots.generate_scatter_plot(country_df, x_metric_column_name, y_metric_column_name)
            st.plotly_chart(scatter_fig, use_container_width=True) if scatter_fig else st.info("No data available for scatter plot for the selected criteria.")
        else:
            st.info("No data available for scatter plot for the selected criteria.")

st.markdown("---")
st.caption("Data Source: World Bank Indicators")