from plotly import graph_objects as go

from dashboard.style import HEATMAP_COLORSCALE, PLOTLY_TEMPLATE


def create_heatmap(data, title, labels=None):
    """Create a single heatmap"""
    
    if labels is None:
        plot_labels = HEATMAP_LABELS
    else:
        plot_labels = labels

    fig = go.Figure(
        data=go.Heatmap(
            z=data,
            x=plot_labels,
            y=plot_labels,
            colorscale=HEATMAP_COLORSCALE,
            showscale=True,
            colorbar=dict(
                title=dict(text="Patients", side="right"),
                tickfont=dict(color="#a0a0b0"),
            ),
            hovertemplate="%{y} × %{x}<br>Patients: %{z}<extra></extra>",
        )
    )

    # Add patient count as text annotations
    annotations = []
    for i, row in enumerate(z_values):
        for j, val in enumerate(row):
            # Ensure we don't go out of bounds if data dimensions don't match labels
            if i < len(plot_labels) and j < len(plot_labels):
                annotations.append(
                    dict(
                        x=plot_labels[j],
                        y=plot_labels[i],
                        text=f"{val:.2f}",
                        showarrow=False,
                        font=dict(color="white" if abs(val) > 0.5 else "#a0a0b0", size=9),
                    )
                )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=450,
        margin=dict(l=60, r=20, t=50, b=50),
        title=dict(text=title, font=dict(size=16), x=0.5),
        xaxis=dict(
            title=dict(text="Patient Satisfaction", font=dict(size=12)),
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=11),
            autorange="reversed",  # Top to bottom for age groups
        ),
        annotations=annotations,
    )

    return fig
