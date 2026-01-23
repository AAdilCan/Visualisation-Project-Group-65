import plotly.express as px
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE, MAIN_COLORS
from dashboard.dash_data import SCATTER_DATA, SERVICES_MAPPING


def create_scatter_plot(selected_services=None, time_range=None):

    # 1. Define dimensions
    dimensions = ["Satisfaction", "Morale", "Refused/Admitted Ratio", "Staff/Patient Ratio"]

    # 2. Filter data based on selection
    df_plot = SCATTER_DATA[dimensions + ["Category", "Week"]]

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
                    "text": "No Service Selected",
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
        hover_data={"Week": True},
        height=800,
    )

    # Style the markers
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
