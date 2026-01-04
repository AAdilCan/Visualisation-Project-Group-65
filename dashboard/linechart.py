import plotly.express as px
from plotly.subplots import go
from dashboard.dash_data import STREAM_DATA
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE, MAIN_COLORS, STREAM_GRAPH_COLORS


def _create_lines(fig, selected_metrics, selected_services, metric_labels):
    """Create lines for each service and selected metric"""
    # Add lines for each service and selected metric
    num_available_colors = len(CHART_COLORS) - 1
    for i, cat in enumerate(selected_services):
        cat_data = STREAM_DATA[STREAM_DATA["Category"] == cat]

        for j, metric in enumerate(selected_metrics):
            # Use different line styles if multiple metrics are selected
            line_style = dict(width=2, color=CHART_COLORS[i % num_available_colors], dash="solid" if j == 0 else "dash")

            fig.add_trace(
                go.Scatter(
                    x=cat_data["Week"],
                    y=cat_data[metric],
                    name=f"{cat} - {metric_labels[metric]}",
                    mode="lines+markers",
                    line=line_style,
                    hovertemplate=(
                        f"<b>{cat}</b><br>{metric_labels[metric]}<br>" "Week: %{x}<br>Value: %{y:.1f}<extra></extra>"
                    ),
                )
            )

    # Add trend lines for each selected metric
    for j, metric in enumerate(selected_metrics):
        avg_by_week = STREAM_DATA.groupby("Week")[metric].mean().reset_index()
        fig.add_trace(
            go.Scatter(
                x=avg_by_week["Week"],
                y=avg_by_week[metric],
                name=f"Avg - {metric_labels[metric]}",
                mode="lines",
                line=dict(color=MAIN_COLORS["text"], width=3, dash="dot" if j == 0 else "longdashdot"),
                hovertemplate=(
                    f"<b>Average {metric_labels[metric]}</b><br>" "Week: %{x}<br>Value: %{y:.1f}<extra></extra>"
                ),
            )
        )


def _create_stream_graph(fig, selected_services):
    """Create stream graph for each service"""
    if not selected_services:
        return

    # Filter data for selected services
    filtered_df = STREAM_DATA[STREAM_DATA["Category"].isin(selected_services)]
    if filtered_df.empty:
        return

    # Sum values by Week for all selected services
    metrics = ["Available Beds", "Patient Requests", "Patient Admissions", "Patient Refusals"]
    stream_df = filtered_df.groupby("Week")[metrics].sum().reset_index()

    # Calculate scaling factor to keep total height around 0-55
    total_per_week = stream_df[metrics].sum(axis=1)
    max_total = total_per_week.max()
    scaling_factor = 55 / max_total if max_total > 0 else 1

    # Center the streamgraph around y = 30
    # Baseline = Center - (0.5 * TotalScaled)
    baseline = 30 - (0.5 * total_per_week * scaling_factor)

    # Add invisible baseline trace to shift the entire stackgroup
    # This centers the subsequent stacked traces around y=30
    fig.add_trace(
        go.Scatter(
            x=stream_df["Week"],
            y=baseline,
            mode="none",
            stackgroup="one",
            showlegend=False,
            hoverinfo="skip",
            fillcolor="rgba(0,0,0,0)",
        )
    )

    # Colors for stream metrics using STREAM_GRAPH_COLORS from style.py
    # We use (len(STREAM_GRAPH_COLORS) - 1) as the limit to avoid the last color (background)
    num_available_colors = len(STREAM_GRAPH_COLORS) - 1
    stream_colors = []
    for i in range(len(metrics)):
        color_hex = STREAM_GRAPH_COLORS[i % num_available_colors]
        rgb = px.colors.hex_to_rgb(color_hex)
        stream_colors.append(f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.3)")

    for i, metric in enumerate(metrics):
        fig.add_trace(
            go.Scatter(
                x=stream_df["Week"],
                y=stream_df[metric] * scaling_factor,
                name=f"Total {metric}",
                stackgroup="one",
                mode="none",
                fillcolor=stream_colors[i % len(stream_colors)],
                hovertemplate=f"<b>{metric}</b><br>Sum: %{{customdata:.0f}}<extra></extra>",
                customdata=stream_df[metric],
            )
        )


def create_line_chart(selected_metrics, selected_services):
    """Create line chart for each service with an average overlay"""

    fig = go.Figure()

    # Metric display names for labels
    metric_labels = {"Patient Satisfaction": "Patient Satisfaction", "Staff Morale": "Staff Morale"}

    _create_stream_graph(fig, selected_services)
    _create_lines(fig, selected_metrics, selected_services, metric_labels)

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=600,
        margin=dict(l=50, r=30, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10)),
        xaxis=dict(rangeslider=dict(visible=True), type="linear"),
        yaxis=dict(title="Metric Value", range=[0, 100], tickvals=[60, 70, 80, 90, 100]),
        hovermode="x unified",
    )

    return fig
