from dash import callback, Output, Input

from dashboard.linechart import create_line_chart
from dashboard.scatterplot_matrix import create_scatter_plot
from dashboard.violinchart import create_violin_chart


@callback(
    Output("line-chart", "figure"),
    [Input("metric-checklist", "value"), Input("services-checklist", "value")],
)
def update_stream_graph(selected_metrics, selected_services):
    """Update stream graph based on metric selection"""
    return create_line_chart(selected_metrics, selected_services)


@callback(Output("violin-chart", "figure"),
          [Input("violin-metric-radio", "value"),
           Input("line-chart", "relayoutData"),
           Input("services-checklist", "value")])
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
            data = data[(data["week"] >= relayout_data["xaxis.range[0]"]) & 
                       (data["week"] <= relayout_data["xaxis.range[1]"])]
    
    # 2. Call chart creator
    # Metric logic is handled inside create_violin_chart
    return create_violin_chart(data, selected_metric, selected_services)


@callback(
    Output("scatter-plot", "figure"),
    [Input("services-checklist", "value"),
     Input("line-chart", "relayoutData")]
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
            time_range = (relayout_data["xaxis.range[0]"], relayout_data["xaxis.range[1]"])

        # If autorange (reset) is triggered, time_range remains None (show all)

    return create_scatter_plot(selected_services, time_range)