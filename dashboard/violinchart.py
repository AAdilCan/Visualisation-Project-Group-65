import plotly.express as px
from plotly.subplots import go
from dashboard.dash_data import SERVICES, SERVICES_MAPPING
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE


def create_violin_chart(data, metric="satisfaction_from_patients", selected_services=None):
    """
    Create violin chart using real data, grouped by Event.
    
    Args:
        data: pandas DataFrame containing the service data.
        metric: The column name to plot distribution for.
        selected_services: List of services to include (optional filter).
    """
    if data is None or data.empty:
        return go.Figure()

    # Filter by services if provided (Global Filter compatibility)
    filtered_data = data.copy()
    if selected_services:
        filtered_data = filtered_data[filtered_data["service"].isin(selected_services)]
        
    if filtered_data.empty:
        return go.Figure()
    
    # Handle "Refused/Admitted Ratio" calculation on the fly
    # metric string from RadioButton will be passed here.
    # If metric is "ratio", we calculate it.
    y_values = None
    y_label = "Value"
    
    if metric == "ratio":
        # Avoid division by zero
        # We can calculate it per row
        # Using numpy for safe division
        import numpy as np
        admitted = filtered_data["patients_admitted"].replace(0, 1) # simple avoidance
        filtered_data["ratio"] = filtered_data["patients_refused"] / admitted
        y_values = filtered_data["ratio"]
        y_label = "Refused/Admitted Ratio"
        plot_metric = "ratio"
    else:
        # For standard metrics
        plot_metric = metric
        if metric == "satisfaction_from_patients":
            y_label = "Patient Satisfaction"
        elif metric == "staff_morale":
            y_label = "Staff Morale"
    
    # Event Colors
    # "flu", "strike", "donation", "none"
    event_colors = {
        "flu": "#ef4444",      # Red
        "strike": "#f59e0b",   # Amber/Orange
        "donation": "#10b981", # Green
        "none": "#6366f1",     # Indigo (Default)
        # Fallback
        "unknown": "#8b5cf6"
    }

    fig = go.Figure()

    # Get unique events
    if "event" not in filtered_data.columns:
        # Fallback if column missing
        return fig
        
    unique_events = filtered_data["event"].unique()

    for event in unique_events:
        event_data = filtered_data[filtered_data["event"] == event]
        color = event_colors.get(str(event).lower(), event_colors["none"])
        event_name = str(event).capitalize()
        
        fig.add_trace(
            go.Violin(
                x=[event_name] * len(event_data),
                y=event_data[plot_metric],
                name=event_name,
                box_visible=True,
                meanline_visible=True,
                fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(color)) + [0.6])}",
                line_color=color,
                opacity=0.8,
                hovertemplate=f"<b>{event_name}</b><br>{y_label}: %{{y:.2f}}<extra></extra>",
            )
        )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=400,
        margin=dict(l=40, r=20, t=30, b=50),
        showlegend=False,
        xaxis_title="Event Type",
        yaxis_title=y_label,
        violinmode="group",
    )

    return fig
