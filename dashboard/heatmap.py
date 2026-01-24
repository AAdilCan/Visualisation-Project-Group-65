from plotly import graph_objects as go

from dashboard.dash_data import get_heatmap_data, SERVICES
from dashboard.style import HEATMAP_COLORSCALE, PLOTLY_TEMPLATE, MAIN_COLORS

# Get border color from MAIN_COLORS
MAIN_COLORS.setdefault("border", "#d0dce8")


def create_heatmap(z_values, x_labels, y_labels, title, selected_services: list[str], current_service: str):
    """Create a single heatmap

    Args:
        z_values: 2D list of values for the heatmap
        x_labels: Labels for the x-axis (columns)
        y_labels: Labels for the y-axis (rows)
        title: Title for the heatmap
        selected_services: List of currently selected services
        current_service: The service ID for this specific heatmap
    """
    # Find max value for determining text color threshold
    max_val = max(max(row) for row in z_values) if z_values and z_values[0] else 1

    # Calculate opacity based on service selection
    # If no services selected (empty list) or current service is selected, show at full opacity
    # Otherwise, fade out
    opacity = 1.0 if not selected_services or current_service in selected_services else 0.3

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
            opacity=opacity,
        )
    )

    # Add patient count as text annotations with dynamic color based on cell darkness
    # Apply same opacity to annotations as the heatmap itself
    annotations = []
    for i, row in enumerate(z_values):
        for j, val in enumerate(row):
            if i < len(y_labels) and j < len(x_labels):
                # Use white text on dark cells (high values), dark text on light cells
                cell_darkness = val / max_val if max_val > 0 else 0
                base_text_color = "#ffffff" if cell_darkness > 0.5 else MAIN_COLORS["text"]

                # Apply opacity to text color by converting to rgba
                if opacity < 1.0:
                    # Convert hex to rgba with opacity
                    if base_text_color == "#ffffff":
                        text_color = f"rgba(255, 255, 255, {opacity})"
                    else:
                        # Parse hex color and apply opacity
                        hex_color = base_text_color.lstrip("#")
                        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                        text_color = f"rgba({r}, {g}, {b}, {opacity})"
                else:
                    text_color = base_text_color

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
            title=dict(
                text="Patient Satisfaction",
                font=dict(size=11, color=MAIN_COLORS["text_secondary"]),
            ),
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


def update_heatmap(fig, z_values, x_labels, y_labels, selected_services: list[str], current_service: str):
    """Updates an existing heatmap figure instead of recreating it.

    Args:
        fig: Existing figure to update
        z_values: 2D list of values for the heatmap
        x_labels: Labels for the x-axis (columns)
        y_labels: Labels for the y-axis (rows)
        selected_services: List of currently selected services
        current_service: The service ID for this specific heatmap
    """

    # Calculate opacity based on service selection
    opacity = 1.0 if not selected_services or current_service in selected_services else 0.3

    # 1. Update the data trace (z-values, x_labels, y_labels, and opacity)
    fig.update_traces(z=z_values, x=x_labels, y=y_labels, opacity=opacity, selector=dict(type="heatmap"))

    # 2. Recalculate annotations efficiently
    max_val = max(max(row) for row in z_values) if z_values and z_values[0] else 1
    new_annotations = []

    for i, row in enumerate(z_values):
        for j, val in enumerate(row):
            if i < len(y_labels) and j < len(x_labels):
                cell_darkness = val / max_val if max_val > 0 else 0
                base_text_color = "#ffffff" if cell_darkness > 0.5 else MAIN_COLORS["text"]

                # Apply opacity to text color
                if opacity < 1.0:
                    if base_text_color == "#ffffff":
                        text_color = f"rgba(255, 255, 255, {opacity})"
                    else:
                        hex_color = base_text_color.lstrip("#")
                        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
                        text_color = f"rgba({r}, {g}, {b}, {opacity})"
                else:
                    text_color = base_text_color

                new_annotations.append(
                    dict(
                        x=x_labels[j],
                        y=y_labels[i],
                        text=str(val),
                        showarrow=False,
                        font=dict(color=text_color, size=10, weight=500),
                    )
                )
    # 3. Use batch_update to push layout changes in one go
    with fig.batch_update():
        fig.layout.annotations = new_annotations

    return fig


heatmap_fig_1 = create_heatmap(*get_heatmap_data("age_bin", "emergency"), "Emergency", SERVICES, "emergency")
heatmap_fig_2 = create_heatmap(*get_heatmap_data("age_bin", "ICU"), "ICU", SERVICES, "ICU")
heatmap_fig_3 = create_heatmap(*get_heatmap_data("age_bin", "surgery"), "Surgery", SERVICES, "surgery")
heatmap_fig_4 = create_heatmap(
    *get_heatmap_data("age_bin", "general_medicine"), "General Medicine", SERVICES, "general_medicine"
)
heatmap_figs = {
    "emergency": heatmap_fig_1,
    "ICU": heatmap_fig_2,
    "surgery": heatmap_fig_3,
    "general_medicine": heatmap_fig_4,
}
