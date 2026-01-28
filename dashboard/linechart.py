import plotly.express as px
from plotly.subplots import go
from dashboard.dash_data import STREAM_DATA, SERVICES
from dashboard.style import (
    CHART_COLORS,
    PLOTLY_TEMPLATE,
    MAIN_COLORS,
    STREAM_GRAPH_COLORS,
)

# Event highlighting constants (similar to scatterplot_matrix.py)
EVENT_MATCH_OPACITY = 0.9
EVENT_NO_MATCH_OPACITY = 0.1
DEFAULT_MARKER_OPACITY = 0.8


def _apply_event_styling(fig: go.Figure, selected_event: str | None) -> None:
    """Apply event-based opacity styling to figure traces.

    Highlights markers for the selected event by adjusting opacity.
    Note: Line opacity cannot be directly controlled in Plotly, so only markers are highlighted.

    Args:
        fig: Plotly figure to style
        selected_event: Event name to highlight (None for default styling)
    """
    if selected_event:
        for trace in fig.data:
            # Only apply styling to traces with customdata containing event info
            # Skip stream graph traces and average traces
            if not hasattr(trace, "customdata") or trace.customdata is None:
                continue

            try:
                # Extract event data from customdata (1D array of events)
                trace_events = trace.customdata

                # Create opacity array for markers based on event match
                opacity_array = [
                    (EVENT_MATCH_OPACITY if str(evt).lower() == selected_event else EVENT_NO_MATCH_OPACITY)
                    for evt in trace_events
                ]

                # Apply opacity to markers
                trace.marker.opacity = opacity_array

            except (AttributeError, IndexError, TypeError) as e:
                # Skip traces that don't have the expected structure
                print(f"Error applying event styling: {e}")
                pass
    else:
        # Reset to default styling when no event is selected
        for trace in fig.data:
            if hasattr(trace, "marker") and trace.marker is not None:
                trace.marker.opacity = DEFAULT_MARKER_OPACITY


def _create_lines(fig, selected_metrics, selected_services, metric_labels):
    """Create lines for each service and selected metric"""
    # Add lines for each service and selected metric
    num_available_colors = len(CHART_COLORS) - 1
    for i, cat in enumerate(selected_services):
        cat_data = STREAM_DATA[STREAM_DATA["Category"] == cat]

        for j, metric in enumerate(selected_metrics):
            # Use different line styles if multiple metrics are selected
            line_style = dict(
                width=2,
                color=CHART_COLORS[i % num_available_colors],
                dash="solid" if j == 0 else "dash",
            )

            # Prepare customdata with event information for event-based highlighting
            # customdata format: just the event value for each point
            customdata = cat_data["event"].tolist()

            fig.add_trace(
                go.Scatter(
                    x=cat_data["Week"],
                    y=cat_data[metric],
                    name=f"{cat} - {metric_labels[metric]}",
                    mode="lines+markers",
                    line=line_style,
                    marker=dict(size=8),  # Make markers more visible
                    customdata=customdata,
                    hovertemplate=(
                        f"<b>{cat}</b><br>{metric_labels[metric]}<br>"
                        "Week: %{x}<br>Value: %{y:.1f}<br>"
                        "Event: %{customdata}<extra></extra>"
                    ),
                )
            )

    # Add trend lines for each selected metric
    for j, metric in enumerate(selected_metrics):
        avg_by_week = STREAM_DATA.groupby("Week")[metric].mean().reset_index()
        fig.add_trace(
            go.Scatter(
                x=avg_by_week["Week"],
                y=avg_by_week[metric],
                name=f"Avg - {metric_labels[metric]}",
                mode="lines",
                line=dict(
                    color=MAIN_COLORS["text"],
                    width=3,
                    dash="dot" if j == 0 else "longdashdot",
                ),
                hovertemplate=(
                    f"<b>Average {metric_labels[metric]}</b><br>" "Week: %{x}<br>Value: %{y:.1f}<extra></extra>"
                ),
            )
        )


def _create_vertical_lines(fig: go.Figure, selected_weeks: list[int]) -> None:
    """Draw vertical lines at specific week positions on the chart.

    Args:
        fig: Plotly figure object to add vertical lines to
        selected_weeks: List of week numbers where vertical lines should be drawn
    """
    shapes, annotations = _create_vertical_lines_shapes(selected_weeks)
    if shapes:
        if fig.layout.shapes:
            fig.layout.shapes.extend(shapes)
        else:
            fig.layout.shapes = shapes
    if annotations:
        if fig.layout.annotations:
            fig.layout.annotations.extend(annotations)
        else:
            fig.layout.annotations = annotations


def _create_vertical_lines_shapes(
    selected_weeks: list[int],
) -> tuple[list[dict], list[dict]]:
    """Create shape and annotation dictionaries for vertical lines (for use inside batch_update).

    Args:
        selected_weeks: List of week numbers where vertical lines should be drawn

    Returns:
        Tuple of (shapes, annotations) to add to fig.layout
    """
    if not selected_weeks:
        return [], []

    # Get unique weeks to avoid duplicate lines
    unique_weeks = sorted(set(int(w) for w in selected_weeks))

    shapes = []
    annotations = []
    for week in unique_weeks:
        # Create shape for the vertical line
        shapes.append(
            dict(
                type="line",
                xref="x",
                yref="paper",
                x0=week,
                x1=week,
                y0=0,
                y1=1,
                line=dict(
                    color=MAIN_COLORS["highlight"],
                    width=2,
                    dash="dash",
                ),
            )
        )
        # Create annotation for the week label
        annotations.append(
            dict(
                text=f"W{week}",
                showarrow=False,
                x=week,
                y=1.02,
                yref="paper",
                xref="x",
                font=dict(size=10, color=MAIN_COLORS["highlight"]),
            )
        )

    return shapes, annotations


def _create_stream_graph(fig, selected_services):
    """Create stream graph for each service"""
    if not selected_services:
        return

    # Filter data for selected services
    filtered_df = STREAM_DATA[STREAM_DATA["Category"].isin(selected_services)]
    if filtered_df.empty:
        return

    # Sum values by Week for all selected services
    metrics = [
        "Available Beds",
        "Patient Requests",
        "Patient Admissions",
        "Patient Refusals",
    ]
    stream_df = filtered_df.groupby("Week")[metrics].sum().reset_index()

    # Calculate scaling factor to keep total height around 0-55
    total_per_week = stream_df[metrics].sum(axis=1)
    max_total = total_per_week.max()
    scaling_factor = 55 / max_total if max_total > 0 else 1

    # Center the streamgraph around y = 30
    # Baseline = Center - (0.5 * TotalScaled)
    baseline = 30 - (0.5 * total_per_week * scaling_factor)

    # Add invisible baseline trace to shift the entire stackgroup
    # This centers the subsequent stacked traces around y=30
    fig.add_trace(
        go.Scatter(
            x=stream_df["Week"],
            y=baseline,
            mode="none",
            stackgroup="one",
            showlegend=False,
            hoverinfo="skip",
            fillcolor=MAIN_COLORS["transparent"],
        )
    )

    # Colors for stream metrics using STREAM_GRAPH_COLORS from style.py
    # We use (len(STREAM_GRAPH_COLORS) - 1) as the limit to avoid the last color (background)
    num_available_colors = len(STREAM_GRAPH_COLORS) - 1
    stream_colors = []
    for i in range(len(metrics)):
        color_hex = STREAM_GRAPH_COLORS[i % num_available_colors]
        rgb = px.colors.hex_to_rgb(color_hex)
        stream_colors.append(f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.3)")

    for i, metric in enumerate(metrics):
        fig.add_trace(
            go.Scatter(
                x=stream_df["Week"],
                y=stream_df[metric] * scaling_factor,
                name=f"Total {metric}",
                stackgroup="one",
                mode="none",
                fillcolor=stream_colors[i % len(stream_colors)],
                hovertemplate=f"<b>{metric}</b><br>Sum: %{{customdata:.0f}}<extra></extra>",
                customdata=stream_df[metric],
            )
        )


def create_line_chart(
    selected_metrics: list[str],
    selected_services: list[str],
    xaxis_range: list[float] | None = None,
    selected_weeks: list[int] | None = None,
    existing_shapes: list | None = None,
    selected_event: str | None = None,
) -> go.Figure:
    """Create line chart for each service with an average overlay.

    Args:
        selected_metrics: List of metrics to display
        selected_services: List of services to display
        xaxis_range: Optional list [min, max] to preserve x-axis zoom state (weeks)
        selected_weeks: Optional list of week numbers to highlight with vertical lines
        existing_shapes: Optional list of shapes to preserve (e.g., vertical lines from previous state)
        selected_event: Optional event name to highlight (dims non-matching points/lines)
    """

    fig = go.Figure()

    # Metric display names for labels
    metric_labels = {
        "Patient Satisfaction": "Patient Satisfaction",
        "Staff Morale": "Staff Morale",
    }

    _create_stream_graph(fig, selected_services)
    _create_lines(fig, selected_metrics, selected_services, metric_labels)

    # Apply event-based highlighting if an event is selected
    _apply_event_styling(fig, selected_event)

    # Add vertical lines for selected weeks from scatter plot
    # If selected_weeks provided, create new vertical lines; otherwise use existing_shapes
    if selected_weeks is not None:
        _create_vertical_lines(fig, selected_weeks)
    elif existing_shapes:
        # Preserve existing vertical lines from previous figure state
        fig.update_layout(shapes=existing_shapes)

    # Build xaxis config, preserving range if provided
    # Default range is 1-52 (weeks) to avoid empty space on the chart
    xaxis_config = dict(rangeslider=dict(visible=True), type="linear", range=[1, 52])
    if xaxis_range is not None:
        xaxis_config["range"] = xaxis_range

    fig.update_layout(
        # uirevision preserves legend visibility and other UI state when constant
        uirevision="line-chart-constant",
        template=PLOTLY_TEMPLATE,
        height=600,
        margin=dict(l=50, r=30, t=30, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
        xaxis=xaxis_config,
        yaxis=dict(title="Metric Value", range=[0, 100], tickvals=[60, 70, 80, 90, 100]),
        hovermode="x unified",
    )

    return fig


def update_line_chart(
    fig: go.Figure,
    selected_metrics: list[str],
    selected_services: list[str],
    xaxis_range: list[float] | None = None,
    selected_weeks: list[int] | None = None,
    existing_shapes: list | None = None,
    selected_event: str | None = None,
) -> go.Figure:
    """Update an existing line chart figure instead of recreating it.

    Args:
        fig: Existing Plotly figure to update
        selected_metrics: List of metrics to display
        selected_services: List of services to display
        xaxis_range: Optional list [min, max] to preserve x-axis zoom state (weeks)
        selected_weeks: Optional list of week numbers to highlight with vertical lines
        existing_shapes: Optional list of shapes to preserve (e.g., vertical lines from previous state)
        selected_event: Optional event name to highlight (dims non-matching points/lines)
    """
    # Metric display names for labels
    metric_labels = {
        "Patient Satisfaction": "Patient Satisfaction",
        "Staff Morale": "Staff Morale",
    }

    # Use batch_update to push all changes in one go
    with fig.batch_update():
        # Clear all existing traces
        fig.data = []

        # Rebuild the chart
        _create_stream_graph(fig, selected_services)
        _create_lines(fig, selected_metrics, selected_services, metric_labels)

        # Apply event-based highlighting if an event is selected
        _apply_event_styling(fig, selected_event)

        # Add vertical lines for selected weeks from scatter plot
        # If selected_weeks provided, create new vertical lines; otherwise use existing_shapes
        if selected_weeks is not None:
            # Clear existing shapes and annotations before adding new ones
            if fig.layout.shapes:
                fig.layout.shapes = []
            if fig.layout.annotations:
                fig.layout.annotations = []

            shapes, annotations = _create_vertical_lines_shapes(selected_weeks)
            if shapes:
                fig.layout.shapes = shapes
            if annotations:
                fig.layout.annotations = annotations
        elif existing_shapes:
            # Preserve existing vertical lines from previous figure state
            # Clear shapes first, then set to existing
            if fig.layout.shapes:
                fig.layout.shapes = []
            fig.layout.shapes = existing_shapes
            # Note: annotations from previous vertical lines are lost when preserving shapes this way
            # This matches the original behavior where only shapes were preserved

        # Build xaxis config, preserving range if provided
        # Default range is 1-52 (weeks) to avoid empty space on the chart
        xaxis_config = dict(rangeslider=dict(visible=True), type="linear", range=[1, 52])
        if xaxis_range is not None:
            xaxis_config["range"] = xaxis_range

        # Update layout settings
        fig.update_layout(
            # uirevision preserves legend visibility and other UI state when constant
            uirevision="line-chart-constant",
            template=PLOTLY_TEMPLATE,
            height=600,
            margin=dict(l=50, r=30, t=30, b=30),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=10),
            ),
            xaxis=xaxis_config,
            yaxis=dict(title="Metric Value", range=[0, 100], tickvals=[60, 70, 80, 90, 100]),
            hovermode="x unified",
        )

    return fig


# Create pre-initialized figure with default values
linechart_fig = create_line_chart(
    selected_metrics=["Patient Satisfaction"],
    selected_services=[SERVICES[0]],
    xaxis_range=None,
    selected_weeks=None,
    existing_shapes=None,
    selected_event=None,
)
