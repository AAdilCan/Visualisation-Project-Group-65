from plotly.graph_objects import Figure

from dash import callback, ctx, Output, Input, State

from dashboard.linechart import linechart_fig, update_line_chart
from dashboard.scatterplot_matrix import scatterplot_fig, update_scatter_plot
from dashboard.violinchart import create_violin_chart
from dashboard.heatmap import heatmap_figs, update_heatmap
from dashboard.dash_data import (
    get_heatmap_data,
    SERVICES_DATA,
    SERVICES,
    SCATTER_DATA,
    SERVICES_MAPPING,
)


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
    dimensions = [
        "Satisfaction",
        "Morale",
        "Refused/Admitted Ratio",
        "Staff/Patient Ratio",
    ]
    df_plot = SCATTER_DATA[dimensions + ["Category", "Week"]]

    if services:
        selected_labels = [
            SERVICES_MAPPING[s] for s in services if s in SERVICES_MAPPING
        ]
        df_plot = df_plot[df_plot["Category"].isin(selected_labels)]

    if time_range:
        start_week, end_week = time_range
        df_plot = df_plot[
            (df_plot["Week"] >= start_week) & (df_plot["Week"] <= end_week)
        ]

    # Return weeks as a list indexed by row position (matching pointIndex)
    return df_plot["Week"].tolist()


@callback(
    [
        Output("heatmap-emergency", "figure"),
        Output("heatmap-icu", "figure"),
        Output("heatmap-surgery", "figure"),
        Output("heatmap-general-medicine", "figure"),
    ],
    [
        Input("heatmap-attribute-radio", "value"),
        Input("line-chart", "relayoutData"),
    ],
    prevent_initial_call=True,
)
def update_heatmaps_cb(attribute, relayout_data):
    """Update all 4 heatmaps based on attribute selection and time range."""
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

    # Define the services and their display names
    figures = []
    for service_id, fig in heatmap_figs.items():
        z_values, x_labels, y_labels = get_heatmap_data(
            attribute, service_id, week_range
        )
        fig = update_heatmap(fig, z_values, x_labels, y_labels)
        figures.append(fig)

    return figures


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
def update_line_chart_cb(
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
            time_range = (
                relayout_data["xaxis.range[0]"],
                relayout_data["xaxis.range[1]"],
            )

    # Determine which input triggered the callback
    triggered_id = ctx.triggered_id

    # Extract selected weeks from scatter plot selection using pointIndex
    # Note: px.scatter_matrix (splom) doesn't support customdata in selectedData,
    # so we use pointIndex to look up weeks from the filtered data
    selected_weeks = None
    existing_shapes = None

    # Check if scatter plot has a non-empty selection
    has_scatter_selection = (
        scatter_selected_data
        and "points" in scatter_selected_data
        and len(scatter_selected_data["points"]) > 0
    )

    if triggered_id == "scatter-plot" and has_scatter_selection:
        # Scatter plot triggered with actual selection - calculate new vertical lines
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
            # Points exist but couldn't map to valid weeks - preserve existing shapes
            if current_fig and "layout" in current_fig:
                existing_shapes = current_fig["layout"].get("shapes", [])
    else:
        # Non-scatter trigger or empty/cleared selection - preserve existing vertical lines
        if current_fig and "layout" in current_fig:
            existing_shapes = current_fig["layout"].get("shapes", [])

    # Use the pre-initialized figure and update it using batch_update
    return update_line_chart(
        linechart_fig,
        selected_metrics,
        services,
        xaxis_range,
        selected_weeks,
        existing_shapes,
    )


@callback(
    Output("violin-chart", "figure"),
    [
        Input("violin-metric-radio", "value"),
        Input("line-chart", "relayoutData"),
        Input("services-checklist", "value"),
    ],
    prevent_initial_call=True,
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
                (data["week"] >= relayout_data["xaxis.range[0]"])
                & (data["week"] <= relayout_data["xaxis.range[1]"])
            ]

    # 2. Call chart creator
    # Metric logic is handled inside create_violin_chart
    return create_violin_chart(data, selected_metric, selected_services)


@callback(
    Output("scatter-plot", "figure"),
    [
        Input("services-checklist", "value"),
        Input("line-chart", "relayoutData"),
        Input("violin-chart", "clickData"),
    ],
)
def update_scatter_plot_cb(selected_services, relayout_data, violin_click_data):
    """
    Update scatter plot based on:
    1. Service selection
    2. Time range selected in Line Chart (Zoom/Pan)
    3. Event selected in Violin Chart (Click)
    """

    # 1. Handle Time Range
    time_range = None
    if relayout_data:
        if "xaxis.range" in relayout_data:
            r = relayout_data["xaxis.range"]
            time_range = (r[0], r[1])
        elif "xaxis.range[0]" in relayout_data and "xaxis.range[1]" in relayout_data:
            time_range = (
                relayout_data["xaxis.range[0]"],
                relayout_data["xaxis.range[1]"],
            )

    # 2. Normalize Services
    services_list = normalize_services(selected_services)

    # 3. Handle Event Selection via Click
    selected_event = None
    trigger_id = ctx.triggered_id

    # If the user clicked the violin chart, we must interpret the click.
    if trigger_id == "violin-chart" and violin_click_data:
        try:
            # We must reconstruct the EXACT event list used by the violin chart
            # to map the x-coordinate index back to the event name.

            # A. Filter data by services (just like the violin chart does)
            # This ensures that if an event is missing from the current view, we don't count it.
            df_temp = SERVICES_DATA[SERVICES_DATA["service"].isin(services_list)]

            # B. Get unique events
            events_found = df_temp["event"].unique()

            # C. Sort alphabetically (Capitalized) excluding 'None'
            sorted_events = sorted(
                [str(e).capitalize() for e in events_found if str(e).lower() != "none"]
            )

            # D. Append 'None' at the end if it exists in the data
            if any(str(e).lower() == "none" for e in events_found):
                sorted_events.append("None")

            # E. Get the clicked coordinate and round to nearest integer index
            click_x = violin_click_data["points"][0]["x"]
            idx = int(round(click_x))

            # F. Map index to name
            if 0 <= idx < len(sorted_events):
                selected_event = sorted_events[idx].lower()

        except (KeyError, IndexError, ValueError):
            selected_event = None

    return update_scatter_plot(scatterplot_fig, services_list, time_range, selected_event)


# =========================================================
# NEW CALLBACK FOR SIDEBAR TOGGLE (UPDATED FOR LEFT SIDE)
# =========================================================
@callback(
    Output("sidebar-overlay", "style"),
    [Input("filter-button", "n_clicks"), Input("close-sidebar", "n_clicks")],
    State("sidebar-overlay", "style"),
    prevent_initial_call=True,
)
def toggle_sidebar(open_clicks, close_clicks, current_style):
    """
    Toggle the sidebar visibility by changing the 'left' CSS property.
    0px = Visible (slid in from left)
    -350px = Hidden (slid out to left)
    """
    ctx_id = ctx.triggered_id

    # Create a copy of the current style to modify to ensure immutability
    new_style = current_style.copy()

    if ctx_id == "filter-button":
        new_style["left"] = "0px"
    elif ctx_id == "close-sidebar":
        new_style["left"] = "-350px"

    return new_style
