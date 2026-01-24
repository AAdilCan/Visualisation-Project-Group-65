import plotly.express as px
import plotly.graph_objects as go
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE, MAIN_COLORS
from dashboard.dash_data import SCATTER_DATA, SERVICES_MAPPING

# Constants
DIMENSIONS = ["Satisfaction", "Morale", "Refused/Admitted Ratio", "Staff/Patient Ratio"]
SCATTER_HEIGHT = 800
EVENT_MATCH_OPACITY = 0.9
EVENT_NO_MATCH_OPACITY = 0.1
DEFAULT_MARKER_SIZE = 6
DEFAULT_MARKER_OPACITY = 0.8
DEFAULT_LINE_WIDTH = 0.5
UNSELECTED_OPACITY = 0.05

# Layout configuration constants
LAYOUT_CONFIG = {
    "template": PLOTLY_TEMPLATE,
    "margin": dict(l=40, r=40, t=40, b=40),
    "legend": dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=10),
    ),
    "dragmode": "select",
    "hovermode": "closest",
}

# Marker styling constants
DEFAULT_MARKER_STYLE = dict(
    size=DEFAULT_MARKER_SIZE,
    opacity=DEFAULT_MARKER_OPACITY,
    line=dict(width=DEFAULT_LINE_WIDTH, color="white"),
)
UNSELECTED_MARKER_STYLE = dict(opacity=UNSELECTED_OPACITY, color="grey")

# Empty figure annotation
EMPTY_FIGURE_ANNOTATION = {
    "text": "No Data (Check Filters)",
    "xref": "paper",
    "yref": "paper",
    "showarrow": False,
    "font": {"size": 20, "color": "white"},
}


def _filter_scatter_data(selected_services=None, time_range=None):
    """Filter scatter plot data based on service and time range selections.

    Args:
        selected_services: Optional list of service IDs to filter by
        time_range: Optional tuple (start_week, end_week) to filter by time

    Returns:
        Filtered DataFrame
    """
    df_plot = SCATTER_DATA[DIMENSIONS + ["Category", "Week", "event"]]

    if selected_services:
        selected_labels = [
            SERVICES_MAPPING[s] for s in selected_services if s in SERVICES_MAPPING
        ]
        df_plot = df_plot[df_plot["Category"].isin(selected_labels)]

    if time_range:
        start_week, end_week = time_range
        df_plot = df_plot[
            (df_plot["Week"] >= start_week) & (df_plot["Week"] <= end_week)
        ]

    return df_plot


def _create_empty_figure():
    """Create an empty figure with 'No Data' message."""
    fig = go.Figure()
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[EMPTY_FIGURE_ANNOTATION],
    )
    return fig


def _apply_event_styling(fig, selected_event):
    """Apply event-based opacity styling to figure traces.

    Args:
        fig: Plotly figure to style
        selected_event: Event name to highlight (None for default styling)
    """
    if selected_event:
        target_event = str(selected_event).lower()

        for trace in fig.data:
            try:
                trace_events = trace.customdata[:, 1]
                opacity_array = [
                    (
                        EVENT_MATCH_OPACITY
                        if str(evt).lower() == target_event
                        else EVENT_NO_MATCH_OPACITY
                    )
                    for evt in trace_events
                ]
                trace.marker.opacity = opacity_array
            except Exception:
                pass
    else:
        fig.update_traces(
            marker=DEFAULT_MARKER_STYLE,
            unselected=dict(marker=UNSELECTED_MARKER_STYLE),
        )


def _apply_layout_config(fig):
    """Apply standard layout configuration to figure.

    Args:
        fig: Plotly figure to configure
    """
    fig.update_layout(**LAYOUT_CONFIG)
    fig.update_xaxes(showgrid=True, gridcolor=MAIN_COLORS["grid"])
    fig.update_yaxes(showgrid=True, gridcolor=MAIN_COLORS["grid"])


def _build_scatter_matrix(df_plot):
    """Build scatter matrix from filtered data.

    Args:
        df_plot: Filtered DataFrame with scatter plot data

    Returns:
        Plotly figure with scatter matrix
    """
    fig = px.scatter_matrix(
        df_plot,
        dimensions=DIMENSIONS,
        color="Category",
        color_discrete_sequence=CHART_COLORS,
        hover_data={"Week": True, "event": True},
        height=SCATTER_HEIGHT,
    )
    return fig


def create_scatter_plot(selected_services=None, time_range=None, selected_event=None):
    """Create a new scatter plot figure.

    Args:
        selected_services: Optional list of service IDs to filter by
        time_range: Optional tuple (start_week, end_week) to filter by time
        selected_event: Optional event name to highlight

    Returns:
        Plotly figure with scatter matrix
    """
    df_plot = _filter_scatter_data(selected_services, time_range)

    if df_plot.empty:
        return _create_empty_figure()

    fig = _build_scatter_matrix(df_plot)
    _apply_event_styling(fig, selected_event)
    _apply_layout_config(fig)

    return fig


def update_scatter_plot(
    fig, selected_services=None, time_range=None, selected_event=None
):
    """Updates an existing scatter plot figure instead of recreating it.

    Args:
        fig: Existing Plotly figure to update
        selected_services: Optional list of service IDs to filter by
        time_range: Optional tuple (start_week, end_week) to filter by time
        selected_event: Optional event name to highlight

    Returns:
        Updated Plotly figure
    """
    df_plot = _filter_scatter_data(selected_services, time_range)

    with fig.batch_update():
        fig.data = []

        if df_plot.empty:
            fig.update_layout(
                template=PLOTLY_TEMPLATE,
                xaxis={"visible": False},
                yaxis={"visible": False},
                annotations=[EMPTY_FIGURE_ANNOTATION],
            )
            return fig

        new_fig = _build_scatter_matrix(df_plot)
        for trace in new_fig.data:
            fig.add_trace(trace)

        _apply_event_styling(fig, selected_event)
        _apply_layout_config(fig)

    return fig


# Create pre-initialized figure with default values
scatterplot_fig = create_scatter_plot()
