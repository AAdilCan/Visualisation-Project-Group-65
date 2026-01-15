import plotly.express as px
from plotly.subplots import go
from dashboard.dash_data import SERVICES, SERVICES_MAPPING
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE


def create_violin_chart(
    data, metric="satisfaction_from_patients", selected_services=None
):
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
    if selected_services is None:
        selected_services = SERVICES

    filtered_data = filtered_data[filtered_data["service"].isin(selected_services)]

    # Handle "Refused/Admitted Ratio" calculation on the fly
    # metric string from RadioButton will be passed here.
    # If metric is "ratio", we calculate it.
    y_label = "Value"

    if metric == "ratio":
        # Avoid division by zero
        # We can calculate it per row
        # Using numpy for safe division
        import numpy as np

        admitted = filtered_data["patients_admitted"].replace(0, 1)  # simple avoidance
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

    # Define colors for services to distinguish them
    # Using CHART_COLORS cyclically
    service_colors = {}
    for i, service in enumerate(SERVICES_MAPPING.keys()):
        service_colors[service] = CHART_COLORS[i % len(CHART_COLORS)]

    fig = go.Figure()

    # Pre-process event names for cleaner X-axis
    if "event" not in filtered_data.columns:
        return fig
    
    # Capitalize events for display
    filtered_data["event_display"] = filtered_data["event"].apply(lambda x: str(x).capitalize())

    # --- Manual X-Axis Positioning ---
    # To center 'None' while splitting others, we use violinmode='overlay' and manual X offsets.
    
    # Define active and none event data
    none_event_data = filtered_data[filtered_data["event"].astype(str).str.lower() == "none"]
    active_event_data = filtered_data[filtered_data["event"].astype(str).str.lower() != "none"]

    unique_events = sorted(
        [e for e in filtered_data["event_display"].unique() if e.lower() != "none"]
    )
    if not none_event_data.empty:
        unique_events.append("None")
    
    event_map = {evt: i for i, evt in enumerate(unique_events)}
    
    # Calculate offsets for active services
    num_services = len(selected_services)
    total_group_width = 0.8
    # Width of each individual violin in the group
    violin_width = total_group_width / max(1, num_services)
    
    # Calculate center offsets for each service position
    # This centers the group of violins around the integer tick
    service_offsets = {}
    for i, service in enumerate(selected_services):
        # Start from left edge, add half width to get center of first violin, etc.
        offset = -(total_group_width / 2) + (violin_width / 2) + (i * violin_width)
        service_offsets[service] = offset

    # 1. Traces for Active Events (Flu, Strike, etc.) - Split by Service
    for service in selected_services:
        # Filter for this service within active events
        service_data = active_event_data[active_event_data["service"] == service]
        
        if service_data.empty:
            continue
            
        service_name = SERVICES_MAPPING.get(service, service)
        color = service_colors.get(service, "#6366f1")

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
                opacity=0.6,
                width=violin_width, # Explicit width to prevent overlap
                points=False, # Disable points to reduce clutter in overlay mode or keep if preferred
                hovertemplate=f"<b>{service_name}</b><br>{y_label}: %{{y:.2f}}<extra></extra>",
            )
        )

    # 2. Trace for "None" Event - Aggregated & Centered
    if not none_event_data.empty:
        agg_name = "All Services (None)"
        agg_color = "#6366f1"
        
        # Map events to integers (No offset for centering)
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
                opacity=0.6,
                width=0.8, # Full width for aggregated
                points=False,
                hovertemplate=f"<b>{agg_name}</b><br>{y_label}: %{{y:.2f}}<extra></extra>",
                showlegend=False
            )
        )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=400,
        margin=dict(l=40, r=20, t=30, b=50),
        showlegend=True, 
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="Event Type",
        yaxis_title=y_label,
        violinmode="overlay", # KEY: Manual positioning
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(unique_events))),
            ticktext=unique_events
        )
    )

    return fig
