from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE
from dashboard.dash_data import SCATTER_DATA
import plotly.express as px


def create_scatter_plot():
    """Create interactive scatter plot"""
    fig = px.scatter(
        SCATTER_DATA,
        x="X_Value",
        y="Y_Value",
        color="Category",
        size="Size",
        hover_data=["Performance"],
        color_discrete_sequence=CHART_COLORS,
    )

    fig.update_traces(
        marker=dict(opacity=0.7, line=dict(width=1, color="white")),
        hovertemplate="<b>%{customdata[0]:.1f}% Performance</b><br>X: %{x:.1f}<br>Y: %{y:.1f}<extra></extra>",
    )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=450,
        margin=dict(l=50, r=30, t=30, b=50),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10)),
        xaxis_title="X Value",
        yaxis_title="Y Value",
    )

    return fig
