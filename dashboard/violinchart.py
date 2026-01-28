from plotly.subplots import go
from dashboard.dash_data import EVENT_MAP, EVENTS, METRIC_DISPLAY_NAME, SERVICES, SERVICES_MAPPING, VIOLIN_DATA
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE, VIOLIN_CHART_COLORS


def _calculate_violin_offsets(selected_services, total_group_width=0.8):
    """
    Calculate x-axis positioning offsets for violin plots.
    """
    num_services = len(selected_services)
    violin_width = total_group_width / max(1, num_services)

    # Calculate center offsets for each service position
    service_offsets = {}
    for i, service in enumerate(selected_services):
        offset = -(total_group_width / 2) + (violin_width / 2) + (i * violin_width)
        service_offsets[service] = offset

    return service_offsets, violin_width


def _add_violin_traces(
    fig,
    selected_services,
    service_colors,
    service_offsets,
    violin_width,
    metric,
    y_label,
):
    """
    Add violin traces for ALL events (including None), split by service.
    """
    for service in selected_services:
        service_data = VIOLIN_DATA[VIOLIN_DATA["service"] == service]

        if service_data.empty:
            continue

        service_name = SERVICES_MAPPING.get(service, service)
        color = service_colors.get(service, CHART_COLORS[0])

        # Map events to integers and add offset
        x_base = service_data["event"].map(EVENT_MAP)
        x_values = x_base + service_offsets[service]

        fig.add_trace(
            go.Violin(
                x=x_values,
                y=service_data[metric],
                name=service_name,
                legendgroup=service_name,
                scalegroup=service_name,
                box_visible=True,
                meanline_visible=True,
                line_color=color,
                fillcolor=color,
                opacity=VIOLIN_CHART_COLORS["opacity"],
                width=violin_width,
                points=False,
                # --- NEW: Add customdata for correct hover info ---
                customdata=service_data["event"],
                hovertemplate=(
                    f"<b>{service_name}</b><br>" "Event: %{{customdata}}<br>" f"{y_label}: %{{y:.2f}}<extra></extra>"
                ),
            )
        )


def _configure_layout(fig, y_label, unique_events):
    """
    Configure figure layout with proper styling.
    """
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=400,
        margin=dict(l=40, r=20, t=30, b=50),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Event Type",
        yaxis_title=y_label,
        violinmode="overlay",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(unique_events))),
            ticktext=unique_events,
        ),
    )


def create_violin_chart(metric: str, selected_services: list[str]) -> go.Figure:
    """Create violin chart using real data, grouped by Event.

    Args:
        metric: Metric to display on y-axis
        selected_services: List of services to display
    """
    # Calculate metric and get y-axis label
    y_label = METRIC_DISPLAY_NAME[metric]

    # Get service colors from style.py
    service_colors = {service: CHART_COLORS[i % len(CHART_COLORS)] for i, service in enumerate(SERVICES_MAPPING.keys())}

    # Calculate violin positioning offsets
    service_offsets, violin_width = _calculate_violin_offsets(selected_services)

    # Create figure
    fig = go.Figure()

    # Add traces (Handles both Active events and None events identically)
    _add_violin_traces(
        fig=fig,
        selected_services=selected_services,
        service_colors=service_colors,
        service_offsets=service_offsets,
        violin_width=violin_width,
        metric=metric,
        y_label=y_label,
    )

    # Configure layout
    _configure_layout(fig=fig, y_label=y_label, unique_events=EVENTS)

    return fig


def update_violin_chart(fig: go.Figure, metric: str, selected_services: list[str]) -> go.Figure:
    """Update an existing violin chart figure instead of recreating it.

    Args:
        fig: Existing Plotly figure to update
        metric: Metric to display on y-axis
        selected_services: List of services to display

    Returns:
        Updated Plotly figure
    """
    # Calculate metric and get y-axis label
    y_label = METRIC_DISPLAY_NAME[metric]

    # Get service colors from style.py
    service_colors = {service: CHART_COLORS[i % len(CHART_COLORS)] for i, service in enumerate(SERVICES_MAPPING.keys())}

    # Calculate violin positioning offsets
    service_offsets, violin_width = _calculate_violin_offsets(selected_services)

    # Use batch_update to push all changes in one go
    with fig.batch_update():
        # Clear all existing traces
        fig.data = []

        # Rebuild the chart
        _add_violin_traces(
            fig=fig,
            selected_services=selected_services,
            service_colors=service_colors,
            service_offsets=service_offsets,
            violin_width=violin_width,
            metric=metric,
            y_label=y_label,
        )

        # Configure layout
        _configure_layout(fig=fig, y_label=y_label, unique_events=EVENTS)

    return fig


# Create pre-initialized figure with default values
violin_fig = create_violin_chart(
    metric="satisfaction_from_patients",
    selected_services=SERVICES,
)
