from plotly import graph_objects as go

from dashboard.style import HEATMAP_COLORSCALE, PLOTLY_TEMPLATE


def create_heatmap(z_values, x_labels, y_labels, title):
    """Create a heatmap with patient count data.
    
    Args:
        z_values: 2D list of patient counts
        x_labels: Labels for x-axis (satisfaction bins)
        y_labels: Labels for y-axis (age bins or length of stay)
        title: Title for the heatmap
    """
    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=x_labels,
            y=y_labels,
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
            annotations.append(
                dict(
                    x=x_labels[j],
                    y=y_labels[i],
                    text=str(val),
                    showarrow=False,
                    font=dict(color="white" if val > 15 else "#a0a0b0", size=10),
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
