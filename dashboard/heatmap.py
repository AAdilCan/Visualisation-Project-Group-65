from plotly import graph_objects as go

from dashboard.style import HEATMAP_COLORSCALE, PLOTLY_TEMPLATE, MAIN_COLORS

# Get border color from MAIN_COLORS
MAIN_COLORS.setdefault("border", "#d0dce8")


def create_heatmap(z_values, x_labels, y_labels, title):
    """Create a single heatmap

    Args:
        z_values: 2D list of values for the heatmap
        x_labels: Labels for the x-axis (columns)
        y_labels: Labels for the y-axis (rows)
        title: Title for the heatmap
    """
    # Find max value for determining text color threshold
    max_val = max(max(row) for row in z_values) if z_values and z_values[0] else 1

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=x_labels,
            y=y_labels,
            colorscale=HEATMAP_COLORSCALE,
            showscale=True,
            colorbar=dict(
                title=dict(text="Patients", side="right", font=dict(color=MAIN_COLORS["text"])),
                tickfont=dict(color=MAIN_COLORS["text_secondary"]),
                outlinecolor=MAIN_COLORS["border"],
                outlinewidth=1,
            ),
            hovertemplate="%{y} × %{x}<br>Patients: %{z}<extra></extra>",
        )
    )

    # Add patient count as text annotations with dynamic color based on cell darkness
    annotations = []
    for i, row in enumerate(z_values):
        for j, val in enumerate(row):
            if i < len(y_labels) and j < len(x_labels):
                # Use white text on dark cells (high values), dark text on light cells
                cell_darkness = val / max_val if max_val > 0 else 0
                text_color = "#ffffff" if cell_darkness > 0.5 else MAIN_COLORS["text"]
                annotations.append(
                    dict(
                        x=x_labels[j],
                        y=y_labels[i],
                        text=str(val),
                        showarrow=False,
                        font=dict(color=text_color, size=10, weight=500),
                    )
                )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        margin=dict(l=60, r=20, t=50, b=50),
        title=dict(text=title, font=dict(size=14, color=MAIN_COLORS["text"]), x=0.5),
        xaxis=dict(
            title=dict(text="Patient Satisfaction", font=dict(size=11, color=MAIN_COLORS["text_secondary"])),
            tickfont=dict(size=10, color=MAIN_COLORS["text_secondary"]),
            linecolor=MAIN_COLORS["border"],
            linewidth=1,
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=10, color=MAIN_COLORS["text_secondary"]),
            autorange="reversed",
            linecolor=MAIN_COLORS["border"],
            linewidth=1,
        ),
        annotations=annotations,
    )

    return fig
