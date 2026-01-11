from dash import callback, Output, Input, State

from dashboard.linechart import create_line_chart
from dashboard.scatterplot_matrix import create_scatter_plot
from dashboard.violinchart import create_violin_chart
from dashboard.heatmap import create_heatmap
from dashboard.dash_data import get_heatmap_data, SERVICES_MAPPING, SERVICES


def normalize_services(selected_services):
    """Convert selected_services to actual service list, handling 'all' option."""
    if not selected_services or "all" in selected_services:
        return SERVICES  # Return all services
    return selected_services


@callback(
    Output("heatmap-main", "figure"),
    [
        Input("heatmap-attribute-radio", "value"),
        Input("services-checklist", "value"),
        Input("line-chart", "relayoutData"),
    ],
)
def update_heatmap(attribute, selected_services, relayout_data):
    """Update heatmap based on attribute, service selection, and time range."""

    # Extract week range from line chart selection
    week_range = None
    if relayout_data:
        if "xaxis.range" in relayout_data:
            r = relayout_data["xaxis.range"]
            week_range = (r[0], r[1])
        elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
            week_range = (
                relayout_data["xaxis.range[0]"],
                relayout_data["xaxis.range[1]"],
            )
        # If autorange (reset) is triggered, week_range remains None (show all)

    # Get heatmap data with filters applied
    z_values, x_labels, y_labels = get_heatmap_data(
        attribute, selected_services, week_range
    )

    # Create dynamic title
    if attribute == "age_bin":
        attr_name = "Age Group"
    else:
        attr_name = "Length of Stay (Days)"

    # Determine service name for title
    if not selected_services or "all" in selected_services:
        service_name = "All Services"
    elif len(selected_services) == 1:
        service_name = SERVICES_MAPPING.get(selected_services[0], selected_services[0])
    else:
        service_name = f"{len(selected_services)} Services"

    # Add week range to title if filtered
    if week_range:
        week_info = f", Weeks {int(week_range[0])}-{int(week_range[1])}"
    else:
        week_info = ""

    title = f"{attr_name} vs Patient Satisfaction ({service_name}{week_info})"

    return create_heatmap(z_values, x_labels, y_labels, title)


@callback(
    Output("line-chart", "figure"),
    [Input("metric-checklist", "value"), Input("services-checklist", "value")],
    [State("line-chart", "relayoutData")],
)
def update_stream_graph(selected_metrics, selected_services, relayout_data):
    """Update stream graph based on metric selection, preserving x-axis range (weeks)"""
    # Normalize services to handle 'all' option
    services = normalize_services(selected_services)

    # Extract x-axis range from relayout_data to preserve zoom/pan state
    xaxis_range = None
    if relayout_data:
        if "xaxis.range" in relayout_data:
            xaxis_range = relayout_data["xaxis.range"]
        elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
            xaxis_range = [
                relayout_data["xaxis.range[0]"],
                relayout_data["xaxis.range[1]"],
            ]

    return create_line_chart(selected_metrics, services, xaxis_range)


@callback(
    Output("violin-chart", "figure"),
    [
        Input("violin-metric-radio", "value"),
        Input("line-chart", "relayoutData"),
        Input("services-checklist", "value"),
    ],
)
def update_violin_chart(selected_metric, relayout_data, selected_services):
    """
    Update violin chart based on:
    1. Metric selection (Radio Button: Satisfaction, Morale, Ratio)
    2. Global Time Range (from Line Chart zoom/pan)
    3. Service selection (Global filter)
    """
    from dashboard.dash_data import SERVICES_DATA, SERVICES_MAPPING

    # 1. Filter by Time Range (if available)
    data = SERVICES_DATA.copy()

    if relayout_data:
        # Check for range updates
        if "xaxis.range" in relayout_data:
            r = relayout_data["xaxis.range"]
            data = data[(data["week"] >= r[0]) & (data["week"] <= r[1])]
        elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
            data = data[
                (data["week"] >= relayout_data["xaxis.range[0]"])
                & (data["week"] <= relayout_data["xaxis.range[1]"])
            ]

    # 2. Call chart creator
    # Metric logic is handled inside create_violin_chart
    return create_violin_chart(data, selected_metric, selected_services)


@callback(
    Output("scatter-plot", "figure"),
    [Input("services-checklist", "value"), Input("line-chart", "relayoutData")],
)
def update_scatter_plot(selected_services, relayout_data):
    """
    Update scatter plot based on:
    1. Service selection
    2. Time range selected in Line Chart (Zoom/Pan)
    """

    time_range = None

    # Check if the trigger was the line chart zoom/pan
    if relayout_data:
        # relayoutData keys vary depending on interaction:
        # 1. 'xaxis.range': [min, max] (Standard zoom)
        # 2. 'xaxis.range[0]': min (Partial update)
        # 3. 'xaxis.autorange': True (Double click reset)

        if "xaxis.range" in relayout_data:
            r = relayout_data["xaxis.range"]
            time_range = (r[0], r[1])

        elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
            time_range = (
                relayout_data["xaxis.range[0]"],
                relayout_data["xaxis.range[1]"],
            )

        # If autorange (reset) is triggered, time_range remains None (show all)

    # Normalize services to handle 'all' option
    services = normalize_services(selected_services)

    return create_scatter_plot(services, time_range)
