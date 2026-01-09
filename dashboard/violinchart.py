import plotly.express as px
from plotly.subplots import go
from dashboard.dash_data import SERVICES, VIOLIN_DATA
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE


def create_violin_chart(selected_quarter=None):
    """Create violin chart"""
    data = VIOLIN_DATA if selected_quarter is None else VIOLIN_DATA[VIOLIN_DATA["Quarter"] == selected_quarter]

    fig = go.Figure()

    for i, cat in enumerate(SERVICES):
        cat_data = data[data["Category"] == cat]["Value"]
        fig.add_trace(
            go.Violin(
                y=cat_data,
                name=cat,
                box_visible=True,
                meanline_visible=True,
                fillcolor=f"rgba{tuple(list(px.colors.hex_to_rgb(CHART_COLORS[i])) + [0.6])}",
                line_color=CHART_COLORS[i],
                opacity=0.8,
                hovertemplate="<b>%{x}</b><br>Value: %{y:.1f}<extra></extra>",
            )
        )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=400,
        margin=dict(l=50, r=30, t=30, b=50),
        showlegend=False,
        xaxis_title="Category",
        yaxis_title="Distribution Value",
        violinmode="group",
    )

    return fig
