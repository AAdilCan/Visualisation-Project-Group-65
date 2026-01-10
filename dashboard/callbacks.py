from dash import callback, Output, Input

from dashboard.linechart import create_line_chart
from dashboard.scatterplot_matrix import create_scatter_plot
from dashboard.violinchart import create_violin_chart
from dashboard.heatmap import create_heatmap
from dashboard.dash_data import get_heatmap_data, SERVICES_MAPPING


@callback(
    Output("heatmap-main", "figure"),
    [Input("heatmap-attribute-radio", "value"),
     Input("heatmap-service-dropdown", "value")]
)
def update_heatmap(attribute, service):
    """Update heatmap based on attribute and service selection."""
    z_values, x_labels, y_labels = get_heatmap_data(attribute, service)
    
    # Create dynamic title
    if attribute == "age_bin":
        attr_name = "Age Group"
    else:
        attr_name = "Length of Stay (Days)"
    
    service_name = SERVICES_MAPPING.get(service, "All Services")
    title = f"{attr_name} vs Patient Satisfaction ({service_name})"
    
    return create_heatmap(z_values, x_labels, y_labels, title)


@callback(
    Output("line-chart", "figure"),
    [Input("metric-checklist", "value"), Input("services-checklist", "value")],
)
def update_stream_graph(selected_metrics, selected_services):
    """Update stream graph based on metric selection"""
    return create_line_chart(selected_metrics, selected_services)


@callback(Output("violin-chart", "figure"),
          [Input("quarter-dropdown", "value"),
           Input("metric-checklist", "value"),
           Input("services-checklist", "value")])
def update_violin_chart(quarter, selected_metrics, selected_services):
    """
    Update violin chart based on:
    1. Quarter selection (Local filter)
    2. Metric selection (Global filter - from Line Chart side)
    3. Service selection (Global filter)
    """
    from dashboard.dash_data import SERVICES_DATA, SERVICES_MAPPING

    # Filter data by Quarter if needed
    data = SERVICES_DATA.copy()
    if quarter != "all":
        # Check if SERVICES_DATA has 'week' or date column to derive quarter
        # The sample data generation in dash_data.py generates weeks.
        # We need to map weeks to quarters.
        # Week 1-13: Q1, 14-26: Q2, 27-39: Q3, 40-52: Q4
        
        # Add a helper to get quarter from week
        def get_quarter(week):
            if week <= 13: return "Q1"
            elif week <= 26: return "Q2"
            elif week <= 39: return "Q3"
            else: return "Q4"
            
        # Ensure 'week' column exists (it's named 'week' in CSV, usually lowercase)
        # Check dash_data.py: "SERVICES_DATA = pd.read_csv(...)"
        # And "SCATTER_DATA.rename(..., 'week': 'Week')" implies original is 'week'
        # But 'violinchart.py' code was using "Quarter" column from random data.
        # We need to compute it.
        if "week" in data.columns:
            data["Quarter"] = data["week"].apply(get_quarter)
            data = data[data["Quarter"] == quarter]
    
    # Determine which metric to plot
    # selected_metrics is a list, e.g., ["Patient Satisfaction", "Staff Morale"]
    # We default to Satisfaction if available, else Morale, else fallback
    metric_col = "satisfaction_from_patients"
    
    if selected_metrics:
        if "Patient Satisfaction" in selected_metrics:
            metric_col = "satisfaction_from_patients"
        elif "Staff Morale" in selected_metrics:
            metric_col = "staff_morale"
    
    return create_violin_chart(data, metric_col, selected_services)


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