import plotly.express as px
import numpy as np
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE, MAIN_COLORS
from dashboard.dash_data import SCATTER_DATA, SERVICES_MAPPING


def create_scatter_plot(selected_services=None, time_range=None, selected_event=None):
    # 1. Define dimensions
    dimensions = ["Satisfaction", "Morale", "Refused/Admitted Ratio", "Staff/Patient Ratio"]

    # 2. Filter data based on selection
    # NOTE: We include 'event' here for hover/styling, but we DO NOT filter rows by event anymore.
    df_plot = SCATTER_DATA[dimensions + ["Category", "Week", "event"]]

    if selected_services:
        # Map IDs to Labels
        selected_labels = [SERVICES_MAPPING[s] for s in selected_services if s in SERVICES_MAPPING]
        df_plot = df_plot[df_plot["Category"].isin(selected_labels)]

    if time_range:
        start_week, end_week = time_range
        df_plot = df_plot[(df_plot["Week"] >= start_week) & (df_plot["Week"] <= end_week)]

    # Handle empty selection case
    if df_plot.empty:
        import plotly.graph_objects as go

        fig = go.Figure()
        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "No Data (Check Filters)",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 20, "color": "white"},
                }
            ],
        )
        return fig

    # 3. Create Matrix using Plotly Express
    fig = px.scatter_matrix(
        df_plot,
        dimensions=dimensions,
        color="Category",
        color_discrete_sequence=CHART_COLORS,
        # We ensure 'event' is the LAST item in hover_data for easy access in customdata
        hover_data={"Week": True, "event": True},
        height=800,
    )

    # 4. Apply Event Filtering via Visual Styling (Highlight vs Grey out)
    if selected_event:
        target_event = str(selected_event).lower()

        # Iterate over every trace (Category) in the figure
        for trace in fig.data:
            # trace.customdata contains the hover_data columns.
            # structure: [[Week, Event], [Week, Event], ...] based on hover_data order
            try:
                # Extract events from the trace data
                # We assume 'event' is at index 1 because we passed {"Week": True, "event": True}
                trace_events = trace.customdata[:, 1]

                # Create styling arrays based on match
                # Match: Opacity 0.8, Color: (Keep original trace color)
                # No Match: Opacity 0.1, Color: Grey (Optional, but opacity is usually enough)

                opacity_array = []
                for evt in trace_events:
                    if str(evt).lower() == target_event:
                        opacity_array.append(0.9)
                    else:
                        opacity_array.append(0.1)  # Dim non-matching points

                # Update the trace
                trace.marker.opacity = opacity_array

                # Optional: Remove white border from dimmed points to make them really fade away
                # line_width_array = [0.5 if o > 0.5 else 0 for o in opacity_array]
                # trace.marker.line.width = line_width_array

            except Exception:
                # Fallback if customdata structure is unexpected
                pass
    else:
        # Default styling if no event selected
        fig.update_traces(
            marker=dict(size=6, opacity=0.8, line=dict(width=0.5, color="white")),
            unselected=dict(marker=dict(opacity=0.05, color="grey")),
        )

    # 5. Global Layout Configuration
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
        dragmode="select",
        hovermode="closest",
    )

    # 6. Clean up axis grids
    fig.update_xaxes(showgrid=True, gridcolor=MAIN_COLORS["grid"])
    fig.update_yaxes(showgrid=True, gridcolor=MAIN_COLORS["grid"])

    return fig