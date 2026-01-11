from plotly import graph_objects as go

from dashboard.style import HEATMAP_COLORSCALE, PLOTLY_TEMPLATE


def create_heatmap(z_values, x_labels, y_labels, title):
    """Create a single heatmap
    
    Args:
        z_values: 2D list of values for the heatmap
        x_labels: Labels for the x-axis (columns)
        y_labels: Labels for the y-axis (rows)
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
            # Ensure we don't go out of bounds if data dimensions don't match labels
            if i < len(y_labels) and j < len(x_labels):
                annotations.append(
                    dict(
                        x=x_labels[j],
                        y=y_labels[i],
                        text=str(val),
                        showarrow=False,
                        font=dict(color="white" if val > 5 else "#a0a0b0", size=9),
                    )
                )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
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
