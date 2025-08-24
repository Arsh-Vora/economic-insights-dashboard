import streamlit as st
import sys
import os
import src.config as config



sys.path.append(os.path.dirname(__file__))
import src.plots as plots
import os


st.set_page_config(
    page_title="Economic Insights Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Economic Insights Dashboard")
st.markdown("Welcome to the Economic Insights Dashboard! This application provides interactive visualizations and analysis of key economic indicators.")
st.markdown("---")
@st.cache_data
def load_data():
    """
    Loads and caches the transformed economic dataset.
    """
    # Assuming df is loaded from a file or created here
    import src.transform as transform
    try:
        df = transform.build_dataset()
        return df
    except Exception as e:
        st.error(f"An error occurred during data transformation: {e}")
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


metric_display_map = {m['id']: m['display_name'] for m in config.METRICS_CONFIG}
metric_ids = [m['id'] for m in config.METRICS_CONFIG]

metric_id_to_display_name = {metric_id: metric_display_map.get(metric_id, metric_id) for metric_id in metric_ids}
selected_metric_id = st.sidebar.selectbox(
    "Select Metric:",
    options=metric_ids,
    format_func=lambda id: metric_id_to_display_name[id],
    index=0
)

selected_metric_config = next((m for m in config.METRICS_CONFIG if m['id'] == selected_metric_id), None)

if selected_metric_config:
    st.sidebar.info(selected_metric_config['description'])


tab1, tab2, tab3 = st.tabs(["Time Series Explorer", "Metric Relationships", "About"])

with tab1:
    selected_metric_name = metric_display_map.get(selected_metric_id, selected_metric_id)
    st.title(f"{selected_metric_name} Comparison")

    if not selected_countries:
        st.info("Please select at least one country to display the chart.")
    else:
        filtered_df = df[df['country.value'].isin(selected_countries)]

        plot_title = f"{selected_metric_name} for Selected Countries"
        fig = plots.generate_time_series_plot(filtered_df, selected_metric_id, plot_title)
        if fig is None or len(fig.data) == 0:
            st.info("No data available for the selected criteria.")
        else:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        with st.expander("▼ Show Plotted Data"):
            st.dataframe(filtered_df[['date', 'country.value', selected_metric_id]].sort_values(by=['country.value', 'date']))

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
        metrics_to_correlate = [m['id'] for m in config.METRICS_CONFIG]
        if country_df.empty:
            st.info("No data available for the selected country.")
        elif not all(metric in country_df.columns for metric in metrics_to_correlate):
            missing_metrics = [m for m in metrics_to_correlate if m not in country_df.columns]
            st.info(f"Data for the following metrics is missing for {country_for_relationships}: {', '.join(missing_metrics)}. Cannot generate heatmap.")
        else:
            corr_fig = plots.generate_correlation_heatmap(country_df, metrics_to_correlate)
            st.plotly_chart(corr_fig, use_container_width=True) if corr_fig else st.info("No data available for correlation heatmap for the selected country.")

        st.markdown("---")

        st.header("Scatter Plot Explorer")

        x_metric_display_name = st.selectbox(
            "Select X-Axis Metric:",
            options=metric_ids,
            format_func=lambda id: metric_display_map.get(id, id),
            index=0,
            key="scatter_x_metric_select"
        )

        y_metric_display_name = st.selectbox(
            "Select Y-Axis Metric:",
            options=metric_ids,
            format_func=lambda id: metric_display_map.get(id, id),
            index=1,
            key="scatter_y_metric_select"
        )

        if not country_df.empty and x_metric_display_name in country_df.columns and y_metric_display_name in country_df.columns:
            scatter_fig = plots.generate_scatter_plot(country_df, x_metric_display_name, y_metric_display_name)
            st.plotly_chart(scatter_fig, use_container_width=True) if scatter_fig else st.info("No data available for scatter plot for the selected criteria.")
        else:
            st.info("No data available for scatter plot for the selected criteria.")

with tab3:
    st.header("About")
    st.markdown("""
    This dashboard provides a comprehensive analysis of key economic indicators across various countries.
    It allows users to explore time-series data, understand correlations between economic metrics, and visualize relationships through scatter plots.
    
    **Data Source:**
    The data used in this dashboard is sourced from the World Bank Indicators.
    
    **Features:**
    - Interactive time-series plots for selected metrics and countries.
    - Correlation heatmaps to visualize relationships between economic indicators.
    - Scatter plots for exploring pairwise relationships between metrics.
    - Data is transformed and standardized for better analysis.
    
    **Technologies Used:**
    - Python
    - Streamlit for the web application framework.
    - Plotly for interactive visualizations.
    - Pandas for data manipulation.
    """)

st.markdown("---")
st.caption("Data Source: World Bank Indicators")