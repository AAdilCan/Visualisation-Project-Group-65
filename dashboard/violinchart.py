from plotly.subplots import go
from dashboard.dash_data import SERVICES, SERVICES_MAPPING
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE, VIOLIN_CHART_COLORS


def _filter_data_by_services(data, selected_services):
    """
    Filter data by selected services.

    Args:
        data: pandas DataFrame containing the service data.
        selected_services: List of services to include.

    Returns:
        Filtered DataFrame and list of selected services.
    """
    if selected_services is None:
        selected_services = SERVICES

    filtered_data = data.copy()
    filtered_data = filtered_data[filtered_data["service"].isin(selected_services)]

    return filtered_data, selected_services


def _calculate_metric(filtered_data, metric):
    """
    Calculate the appropriate metric and return y-axis label.

    Args:
        filtered_data: pandas DataFrame to process.
        metric: The metric name to calculate.

    Returns:
        Tuple of (processed_data, plot_metric, y_label).
    """
    if metric == "ratio":
        # Avoid division by zero by replacing 0 with 1
        admitted = filtered_data["patients_admitted"].replace(0, 1)
        filtered_data["ratio"] = filtered_data["patients_refused"] / admitted
        return filtered_data, "ratio", "Refused/Admitted Ratio"
    elif metric == "satisfaction_from_patients":
        return filtered_data, metric, "Patient Satisfaction"
    elif metric == "staff_morale":
        return filtered_data, metric, "Staff Morale"
    else:
        return filtered_data, metric, "Value"


def _get_service_colors(selected_services):
    """
    Assign colors to services using CHART_COLORS from style.py.

    Args:
        selected_services: List of service identifiers.

    Returns:
        Dictionary mapping service names to colors.
    """
    service_colors = {}
    for i, service in enumerate(SERVICES_MAPPING.keys()):
        service_colors[service] = CHART_COLORS[i % len(CHART_COLORS)]
    return service_colors


def _prepare_event_data(filtered_data):
    """
    Prepare event data by splitting into 'none' and 'active' events.

    Args:
        filtered_data: pandas DataFrame with event column.

    Returns:
        Tuple of (none_event_data, active_event_data, unique_events, event_map).
    """
    # Capitalize events for display
    filtered_data["event_display"] = filtered_data["event"].apply(lambda x: str(x).capitalize())

    # Split data by event type
    none_event_data = filtered_data[filtered_data["event"].astype(str).str.lower() == "none"]
    active_event_data = filtered_data[filtered_data["event"].astype(str).str.lower() != "none"]

    # Create ordered list of unique events
    unique_events = sorted([e for e in filtered_data["event_display"].unique() if e.lower() != "none"])
    if not none_event_data.empty:
        unique_events.append("None")

    # Map event names to integer positions
    event_map = {evt: i for i, evt in enumerate(unique_events)}

    return none_event_data, active_event_data, unique_events, event_map


def _calculate_violin_offsets(selected_services, total_group_width=0.8):
    """
    Calculate x-axis positioning offsets for violin plots.

    Args:
        selected_services: List of services to create violins for.
        total_group_width: Total width allocated for the group of violins.

    Returns:
        Tuple of (service_offsets, violin_width).
    """
    num_services = len(selected_services)
    violin_width = total_group_width / max(1, num_services)

    # Calculate center offsets for each service position
    # This centers the group of violins around the integer tick
    service_offsets = {}
    for i, service in enumerate(selected_services):
        offset = -(total_group_width / 2) + (violin_width / 2) + (i * violin_width)
        service_offsets[service] = offset

    return service_offsets, violin_width


def _add_active_event_traces(
    fig,
    active_event_data,
    selected_services,
    service_colors,
    service_offsets,
    violin_width,
    event_map,
    plot_metric,
    y_label,
):
    """
    Add violin traces for active events (Flu, Strike, etc.) split by service.

    Args:
        fig: Plotly Figure object to add traces to.
        active_event_data: DataFrame containing active event data.
        selected_services: List of services to plot.
        service_colors: Dictionary mapping services to colors.
        service_offsets: Dictionary mapping services to x-axis offsets.
        violin_width: Width of each violin plot.
        event_map: Dictionary mapping event names to positions.
        plot_metric: Metric column name to plot.
        y_label: Label for y-axis.
    """
    for service in selected_services:
        service_data = active_event_data[active_event_data["service"] == service]

        if service_data.empty:
            continue

        service_name = SERVICES_MAPPING.get(service, service)
        color = service_colors.get(service, CHART_COLORS[0])

        # Map events to integers and add offset
        x_base = service_data["event_display"].map(event_map)
        x_values = x_base + service_offsets[service]

        fig.add_trace(
            go.Violin(
                x=x_values,
                y=service_data[plot_metric],
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
                hovertemplate=f"<b>{service_name}</b><br>{y_label}: %{{y:.2f}}<extra></extra>",
            )
        )


def _add_none_event_trace(fig, none_event_data, event_map, plot_metric, y_label):
    """
    Add aggregated violin trace for 'None' event.

    Args:
        fig: Plotly Figure object to add trace to.
        none_event_data: DataFrame containing 'none' event data.
        event_map: Dictionary mapping event names to positions.
        plot_metric: Metric column name to plot.
        y_label: Label for y-axis.
    """
    if none_event_data.empty:
        return

    agg_name = "All Services (None)"
    agg_color = VIOLIN_CHART_COLORS["aggregated_none"]

    # Map events to integers (no offset for centering)
    x_values = none_event_data["event_display"].map(event_map)

    fig.add_trace(
        go.Violin(
            x=x_values,
            y=none_event_data[plot_metric],
            name=agg_name,
            legendgroup="None",
            scalegroup="None",
            box_visible=True,
            meanline_visible=True,
            line_color=agg_color,
            fillcolor=agg_color,
            opacity=VIOLIN_CHART_COLORS["opacity"],
            width=0.8,
            points=False,
            hovertemplate=f"<b>{agg_name}</b><br>{y_label}: %{{y:.2f}}<extra></extra>",
            showlegend=False,
        )
    )


def _configure_layout(fig, y_label, unique_events):
    """
    Configure figure layout with proper styling.

    Args:
        fig: Plotly Figure object to configure.
        y_label: Label for y-axis.
        unique_events: List of unique event names for x-axis.
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


def create_violin_chart(data, metric="satisfaction_from_patients", selected_services=None):
    """
    Create violin chart using real data, grouped by Event.

    Args:
        data: pandas DataFrame containing the service data.
        metric: The column name to plot distribution for.
        selected_services: List of services to include (optional filter).

    Returns:
        Plotly Figure object containing the violin chart.
    """
    # Early return for empty data
    if data is None or data.empty:
        return go.Figure()

    # Filter data by selected services
    filtered_data, selected_services = _filter_data_by_services(data, selected_services)

    # Calculate metric and get y-axis label
    filtered_data, plot_metric, y_label = _calculate_metric(filtered_data, metric)

    # Check for event column
    if "event" not in filtered_data.columns:
        return go.Figure()

    # Get service colors from style.py
    service_colors = _get_service_colors(selected_services)

    # Prepare event data (split into none/active events)
    none_event_data, active_event_data, unique_events, event_map = _prepare_event_data(filtered_data)

    # Calculate violin positioning offsets
    service_offsets, violin_width = _calculate_violin_offsets(selected_services)

    # Create figure
    fig = go.Figure()

    # Add traces for active events
    _add_active_event_traces(
        fig=fig,
        active_event_data=active_event_data,
        selected_services=selected_services,
        service_colors=service_colors,
        service_offsets=service_offsets,
        violin_width=violin_width,
        event_map=event_map,
        plot_metric=plot_metric,
        y_label=y_label,
    )

    # Add trace for none event
    _add_none_event_trace(
        fig=fig,
        none_event_data=none_event_data,
        event_map=event_map,
        plot_metric=plot_metric,
        y_label=y_label,
    )

    # Configure layout
    _configure_layout(fig=fig, y_label=y_label, unique_events=unique_events)

    return fig
