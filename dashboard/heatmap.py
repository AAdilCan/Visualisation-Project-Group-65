from plotly.subplots import go

from dashboard.dash_data import HEATMAP_LABELS
from dashboard.style import HEATMAP_COLORSCALE, PLOTLY_TEMPLATE


def create_heatmap(data, title):
    """Create a single heatmap"""
    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=HEATMAP_LABELS,
            y=HEATMAP_LABELS,
            colorscale=HEATMAP_COLORSCALE,
            showscale=False,
            hovertemplate="%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>",
        )
    )

    # Add correlation values as text
    annotations = []
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            annotations.append(
                dict(
                    x=HEATMAP_LABELS[j],
                    y=HEATMAP_LABELS[i],
                    text=f"{val:.2f}",
                    showarrow=False,
                    font=dict(color="white" if abs(val) > 0.5 else "#a0a0b0", size=9),
                )
            )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=250,
        margin=dict(l=40, r=20, t=40, b=40),
        title=dict(text=title, font=dict(size=14), x=0.5),
        annotations=annotations,
    )

    return fig
