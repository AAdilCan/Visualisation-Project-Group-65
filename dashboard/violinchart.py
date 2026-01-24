from plotly.subplots import go
from dashboard.dash_data import EVENT_MAP, EVENTS, SERVICES, SERVICES_MAPPING
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE, VIOLIN_CHART_COLORS


def _filter_data_by_services(data, selected_services):
    """
    Filter data by selected services.
    """
    if selected_services is None:
        selected_services = SERVICES

    filtered_data = data
    filtered_data = filtered_data[filtered_data["service"].isin(selected_services)]

    return filtered_data, selected_services


def _calculate_metric(filtered_data, metric):
    """
    Calculate the appropriate metric and return y-axis label.
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
    """
    service_colors = {}
    for i, service in enumerate(SERVICES_MAPPING.keys()):
        service_colors[service] = CHART_COLORS[i % len(CHART_COLORS)]
    return service_colors


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
    data,
    selected_services,
    service_colors,
    service_offsets,
    violin_width,
    plot_metric,
    y_label,
):
    """
    Add violin traces for ALL events (including None), split by service.
    """
    for service in selected_services:
        service_data = data[data["service"] == service]

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
                # --- NEW: Add customdata for correct hover info ---
                customdata=service_data["event"],
                hovertemplate=f"<b>{service_name}</b><br>Event: %{{customdata}}<br>{y_label}: %{{y:.2f}}<extra></extra>",
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


def create_violin_chart(
    data, metric="satisfaction_from_patients", selected_services=None
):
    """
    Create violin chart using real data, grouped by Event.
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

    # # Prepare event data (Unified: 'None' is just another event now)
    # processed_data, unique_events, event_map = _prepare_event_data(filtered_data)

    # Calculate violin positioning offsets
    service_offsets, violin_width = _calculate_violin_offsets(selected_services)

    # Create figure
    fig = go.Figure()

    # Add traces (Handles both Active events and None events identically)
    _add_violin_traces(
        fig=fig,
        data=filtered_data,
        selected_services=selected_services,
        service_colors=service_colors,
        service_offsets=service_offsets,
        violin_width=violin_width,
        # event_map=EVENT_MAP,
        plot_metric=plot_metric,
        y_label=y_label,
    )

    # Configure layout
    _configure_layout(fig=fig, y_label=y_label, unique_events=EVENTS)

    return fig
