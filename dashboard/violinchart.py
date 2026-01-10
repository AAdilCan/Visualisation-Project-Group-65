import plotly.express as px
from plotly.subplots import go
from dashboard.dash_data import SERVICES, SERVICES_MAPPING
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE


def create_violin_chart(data, metric="satisfaction_from_patients", selected_services=None):
    """
    Create violin chart using real data
    
    Args:
        data: pandas DataFrame containing the service data
        metric: The column name to plot distribution for
        selected_services: List of services to include
    """
    if data is None or data.empty:
        return go.Figure()

    # Filter by services if provided
    if selected_services:
        # Convert display names back to service keys if needed or used directly
        # The data 'service' column has keys like 'emergency', 'ICU'
        # The 'Category' column in other places has display names.
        # Let's check what 'selected_services' contains.
        # It comes from services-checklist, which has values like 'emergency', 'ICU' (keys)
        # So we filter on 'service' column.
        filtered_data = data[data["service"].isin(selected_services)].copy()
    else:
        filtered_data = data.copy()
        
    if filtered_data.empty:
        return go.Figure()

    fig = go.Figure()

    # Get unique services present in the filtered data to ensure correct color mapping
    # We map service key to index for color
    unique_services = filtered_data["service"].unique()

    for service_key in unique_services:
        # Get data for this service
        service_data = filtered_data[filtered_data["service"] == service_key]
        
        # Determine color index
        # We find the index of this service in the global SERVICES list to keep colors consistent
        try:
            color_idx = SERVICES.index(service_key) % len(CHART_COLORS)
            color = CHART_COLORS[color_idx]
        except ValueError:
            color = CHART_COLORS[0]

        # Get display name
        display_name = SERVICES_MAPPING.get(service_key, service_key)

        fig.add_trace(
            go.Violin(
                x=[display_name] * len(service_data[metric]),
                y=service_data[metric],
                name=display_name,
                box_visible=True,
                meanline_visible=True,
                fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(color)) + [0.6])}",
                line_color=color,
                opacity=0.8,
                hovertemplate=f"<b>{display_name}</b><br>{metric}: %{{y:.1f}}<extra></extra>",
            )
        )

    # Title update based on metric
    # Map column name to display name for axis
    axis_title = "Value"
    if metric == "satisfaction_from_patients":
        axis_title = "Patient Satisfaction Score"
    elif metric == "staff_morale":
        axis_title = "Staff Morale Score"
    elif "ratio" in metric.lower():
        axis_title = "Ratio"

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=400,
        margin=dict(l=40, r=20, t=30, b=50),
        showlegend=False,
        xaxis_title="Service Category",
        yaxis_title=axis_title,
        violinmode="group",
    )

    return fig
