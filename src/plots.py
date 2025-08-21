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

    
    df_filtered = df.dropna(subset=[metric])

    
    df_sorted = df_filtered.sort_values(by=['country.value', 'date'])

    fig = px.line(df_sorted, x='date', y=metric, color='country.value', title=title)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=metric.replace('_', ' ').title().title()
    )
    return fig

def generate_correlation_heatmap(df: pd.DataFrame, metrics_to_correlate: list):
    """
    Generates an interactive correlation heatmap using Plotly Express.

    Args:
        df (pd.DataFrame): The input DataFrame for a single country.
                           Expected columns: the metrics specified in metrics_to_correlate.
        metrics_to_correlate (list): A list of column names (metrics) to include in the correlation matrix.

    Returns:
        plotly.graph_objects.Figure: A Plotly Figure object for the heatmap.
    """
    if df.empty or not metrics_to_correlate:
        return go.Figure()

    
    
    valid_metrics = [m for m in metrics_to_correlate if m in df.columns]
    if not valid_metrics:
        return go.Figure()
        
    corr_matrix = df[valid_metrics].corr()

    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,  
        aspect="auto",   
        title="Correlation Matrix of Key Economic Indicators"
    )
    fig.update_layout(
        xaxis_title="Metrics",
        yaxis_title="Metrics"
    )
    return fig

def generate_scatter_plot(df: pd.DataFrame, x_metric: str, y_metric: str):
    """
    Generates an interactive scatter plot using Plotly Express.

    Args:
        df (pd.DataFrame): The input DataFrame for a single country.
                           Expected columns: x_metric and y_metric.
        x_metric (str): The name of the column for the x-axis.
        y_metric (str): The name of the column for the y-axis.

    Returns:
        plotly.graph_objects.Figure: A Plotly Figure object for the scatter plot.
    """
    if df.empty or x_metric not in df.columns or y_metric not in df.columns:
        return go.Figure()

    
    fig = px.scatter(
        df,
        x=x_metric,
        y=y_metric,
        hover_name='date', 
        title=f"{y_metric.replace('_', ' ').title()} vs {x_metric.replace('_', ' ').title()}"
    )
    fig.update_layout(
        xaxis_title=x_metric.replace('_', ' ').title(),
        yaxis_title=y_metric.replace('_', ' ').title()
    )
    return fig