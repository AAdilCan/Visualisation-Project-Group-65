from dash import callback, Output, Input

from dashboard.linechart import create_line_chart
from dashboard.violinchart import create_violin_chart


@callback(
    Output("stream-graph", "figure"),
    [Input("metric-checklist", "value")],
)
def update_stream_graph(selected_metrics):
    """Update stream graph based on metric selection"""
    return create_line_chart(selected_metrics)


@callback(Output("violin-chart", "figure"), Input("quarter-dropdown", "value"))
def update_violin_chart(quarter):
    """Update violin chart based on quarter selection"""
    if quarter == "all":
        return create_violin_chart()
    return create_violin_chart(quarter)
