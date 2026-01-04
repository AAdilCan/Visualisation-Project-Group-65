from plotly.subplots import go
from dashboard.dash_data import SERVICES, STREAM_DATA
from dashboard.style import CHART_COLORS, PLOTLY_TEMPLATE


def create_line_chart(selected_metrics):
    """Create line chart for each service with an average overlay"""
    if not selected_metrics:
        selected_metrics = ["patient_satisfaction"]

    fig = go.Figure()

    # Metric display names for labels
    metric_labels = {"patient_satisfaction": "Patient Satisfaction", "staff_morale": "Staff Morale"}

    # Add lines for each service and selected metric
    for i, cat in enumerate(SERVICES):
        cat_data = STREAM_DATA[STREAM_DATA["Category"] == cat]

        for j, metric in enumerate(selected_metrics):
            # Use different line styles if multiple metrics are selected
            line_style = dict(width=2, color=CHART_COLORS[i % len(CHART_COLORS)], dash="solid" if j == 0 else "dash")

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
                line=dict(color="#ffffff", width=3, dash="dot" if j == 0 else "longdashdot"),
                hovertemplate=(
                    f"<b>Average {metric_labels[metric]}</b><br>" "Week: %{x}<br>Value: %{y:.1f}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=550,
        margin=dict(l=50, r=30, t=30, b=100),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10)),
        xaxis=dict(rangeslider=dict(visible=True), type="linear"),
        yaxis_title="Metric Value",
        hovermode="x unified",
    )

    return fig
