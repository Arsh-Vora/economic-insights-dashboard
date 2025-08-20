import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def generate_time_series_plot(df: pd.DataFrame, metric: str, title: str):
    """
    Generates an interactive time-series line plot using Plotly Express.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
                          Expected columns: 'date', 'country.value', and the specified metric.
        metric (str): The name of the column to plot on the y-axis.
        title (str): The title of the plot.

    Returns:
        plotly.graph_objects.Figure: A Plotly Figure object.
    """
    if df.empty:
        return go.Figure()

    # Filter out rows where the metric is NaN to prevent gaps in lines
    df_filtered = df.dropna(subset=[metric])

    # Ensure data is sorted for correct line plotting
    df_sorted = df_filtered.sort_values(by=['country.value', 'date'])

    fig = px.line(df_sorted, x='date', y=metric, color='country.value', title=title)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=metric.replace('_', ' ').title().title()
    )
    return fig