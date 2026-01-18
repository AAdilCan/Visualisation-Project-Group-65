from plotly.graph_objects import Figure

from dash import callback, ctx, Output, Input, State

from dashboard.linechart import create_line_chart
from dashboard.scatterplot_matrix import create_scatter_plot
from dashboard.violinchart import create_violin_chart
from dashboard.heatmap import create_heatmap
from dashboard.dash_data import get_heatmap_data, SERVICES_DATA, SERVICES, SCATTER_DATA, SERVICES_MAPPING


def normalize_services(selected_services: list[str] | None) -> list[str]:
    """Convert selected_services to actual service list."""
    if not selected_services:
        return SERVICES  # Return all services
    return selected_services


def _extract_xaxis_range(relayout_data: dict | None) -> list[float] | None:
    """Extract x-axis range from relayout data."""
    if not relayout_data:
        return None

    if "xaxis.range" in relayout_data:
        return relayout_data["xaxis.range"]
    elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
        return [
            relayout_data["xaxis.range[0]"],
            relayout_data["xaxis.range[1]"],
        ]
    return None


def _get_scatter_week_lookup(
    services: list[str],
    time_range: tuple[float, float] | None,
) -> list[int]:
    """Build a week lookup array matching the scatter plot's filtered data.

    This replicates the same filtering logic used in create_scatter_plot
    so that pointIndex from selectedData can be used to look up weeks.
    """
    dimensions = ["Satisfaction", "Morale", "Refused/Requested Ratio", "Staff/Patient Ratio"]
    df_plot = SCATTER_DATA[dimensions + ["Category", "Week"]]

    if services:
        selected_labels = [SERVICES_MAPPING[s] for s in services if s in SERVICES_MAPPING]
        df_plot = df_plot[df_plot["Category"].isin(selected_labels)]

    if time_range:
        start_week, end_week = time_range
        df_plot = df_plot[(df_plot["Week"] >= start_week) & (df_plot["Week"] <= end_week)]

    # Return weeks as a list indexed by row position (matching pointIndex)
    return df_plot["Week"].tolist()


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

    selected_services = normalize_services(selected_services)

    # Get heatmap data with filters applied
    z_values, x_labels, y_labels = get_heatmap_data(attribute, selected_services, week_range)

    # Create dynamic title
    if attribute == "age_bin":
        attr_name = "Age Group"
    else:
        attr_name = "Length of Stay (Days)"

    title = f"{attr_name} vs Patient Satisfaction"

    return create_heatmap(z_values, x_labels, y_labels, title)


@callback(
    Output("line-chart", "figure"),
    [
        Input("metric-checklist", "value"),
        Input("services-checklist", "value"),
        Input("scatter-plot", "selectedData"),
    ],
    [
        State("line-chart", "relayoutData"),
        State("line-chart", "figure"),
    ],
)
def update_line_chart(
    selected_metrics: list[str],
    selected_services: list[str] | None,
    scatter_selected_data: dict | None,
    relayout_data: dict | None,
    current_fig: dict | None,
) -> Figure:
    """Update line chart based on metric selection and scatter plot selection.

    Preserves legend visibility via uirevision and vertical lines when non-scatter inputs trigger.

    Args:
        selected_metrics: List of selected metrics from checklist
        selected_services: List of selected services from checklist
        scatter_selected_data: Selected data from scatter plot matrix (contains week information)
        relayout_data: Current layout state to preserve zoom/pan
        current_fig: Current figure state to preserve vertical lines (shapes)
    """
    services = normalize_services(selected_services)

    # Extract x-axis range from relayout_data to preserve zoom/pan state
    xaxis_range = _extract_xaxis_range(relayout_data)

    # Extract time range for scatter plot filtering (same logic as update_scatter_plot)
    time_range = None
    if relayout_data:
        if "xaxis.range" in relayout_data:
            r = relayout_data["xaxis.range"]
            time_range = (r[0], r[1])
        elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
            time_range = (relayout_data["xaxis.range[0]"], relayout_data["xaxis.range[1]"])

    # Determine which input triggered the callback
    triggered_id = ctx.triggered_id

    # Extract selected weeks from scatter plot selection using pointIndex
    # Note: px.scatter_matrix (splom) doesn't support customdata in selectedData,
    # so we use pointIndex to look up weeks from the filtered data
    selected_weeks = None
    existing_shapes = None

    if triggered_id == "scatter-plot" and scatter_selected_data and "points" in scatter_selected_data:
        # Scatter plot triggered with a selection - calculate new vertical lines
        week_lookup = _get_scatter_week_lookup(services, time_range)

        weeks = []
        for point in scatter_selected_data["points"]:
            if "pointIndex" in point:
                idx = point["pointIndex"]
                if idx < len(week_lookup):
                    weeks.append(int(week_lookup[idx]))

        if weeks:
            selected_weeks = sorted(set(weeks))
    else:
        # Non-scatter trigger or empty selection - preserve existing vertical lines
        if current_fig and "layout" in current_fig:
            existing_shapes = current_fig["layout"].get("shapes", [])

    return create_line_chart(selected_metrics, services, xaxis_range, selected_weeks, existing_shapes)


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

    # 1. Filter by Time Range (if available)
    data = SERVICES_DATA.copy()

    if relayout_data:
        # Check for range updates
        if "xaxis.range" in relayout_data:
            r = relayout_data["xaxis.range"]
            data = data[(data["week"] >= r[0]) & (data["week"] <= r[1])]
        elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
            data = data[
                (data["week"] >= relayout_data["xaxis.range[0]"]) & (data["week"] <= relayout_data["xaxis.range[1]"])
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

    services = normalize_services(selected_services)

    return create_scatter_plot(services, time_range)
