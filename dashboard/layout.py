from dash import dcc, html

from dashboard.dash_data import (
    get_heatmap_data,
    SERVICES,
    SERVICES_MAPPING,
    SERVICES_DATA,
)
from dashboard.heatmap import create_heatmap
from dashboard.linechart import create_line_chart
from dashboard.scatterplot_matrix import create_scatter_plot
from dashboard.violinchart import create_violin_chart
from dashboard.style import MAIN_COLORS

LINECHART_CARD = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Services Weekly Performance"),
                        html.P("Satisfaction Metrics for services" " against Patient Admissions and Bed Availability"),
                        html.P(
                            "* The scale for the streamgraph " "is not aligned with the metric scores.",
                            style={
                                "color": MAIN_COLORS["text_muted"],
                                "fontSize": "0.75rem",
                                "fontStyle": "italic",
                            },
                        ),
                        html.P(
                            "* Services selection applies to all figures.",
                            style={
                                "color": MAIN_COLORS["text_muted"],
                                "fontSize": "0.75rem",
                                "fontStyle": "italic",
                            },
                        ),
                        html.P(
                            "* Select a window with the slider to filter data on other figures.",
                            style={
                                "color": MAIN_COLORS["text_muted"],
                                "fontSize": "0.75rem",
                                "fontStyle": "italic",
                            },
                        ),
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Services:",
                            style={
                                "color": MAIN_COLORS["text_secondary"],
                                "marginBottom": "8px",
                                "display": "block",
                                "fontSize": "0.8rem",
                            },
                        ),
                        dcc.Checklist(
                            id="services-checklist",
                            options=[{"label": label, "value": service} for service, label in SERVICES_MAPPING.items()],
                            value=[SERVICES[0]],
                            className="custom-checklist",
                        ),
                        html.Label(
                            "Metrics:",
                            style={
                                "color": MAIN_COLORS["text_secondary"],
                                "marginBottom": "8px",
                                "display": "block",
                                "fontSize": "0.8rem",
                            },
                        ),
                        dcc.Checklist(
                            id="metric-checklist",
                            options=[
                                {
                                    "label": "Patient Satisfaction",
                                    "value": "Patient Satisfaction",
                                },
                                {"label": "Staff Morale", "value": "Staff Morale"},
                            ],
                            value=["Patient Satisfaction"],
                            className="custom-checklist",
                        ),
                    ],
                    className="services-filters-container",
                ),
            ],
            className="graph-card-header",
        ),
        dcc.Graph(
            id="line-chart",
            figure=create_line_chart(["Patient Satisfaction"], [SERVICES[0]]),
            config={"responsive": False},
            style={"height": "600px"},
        ),
    ],
    className="graph-card",
    style={
        "background": "transparent",
        "border": "none",
        "boxShadow": "none",
        "padding": "0",
    },
)


SCATTER_PLOT_CARD = html.Div(
    [
        html.Div(
            [
                html.H3("Scatter Plot Analysis"),
                html.P("Correlation Matrix of Service Metrics"),
            ]
        ),
        dcc.Graph(
            id="scatter-plot",
            figure=create_scatter_plot(),
            config={"responsive": False},
            # Increased height to 750px. This allows the 4x4 matrix to be readable
            # and roughly matches the height of the 2x2 Heatmaps block next to it.
            style={"height": "750px"},
        ),
    ],
    className="graph-card",
    # Ensure the card itself fills the height of the grid cell
    style={"height": "100%"},
)


HEATMAPS_CONTAINER = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Patient Satisfaction Heatmaps"),
                        html.P("Distribution of patients across satisfaction levels by service"),
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Group By:",
                            style={
                                "color": MAIN_COLORS["text_secondary"],
                                "marginBottom": "8px",
                                "display": "block",
                                "fontSize": "0.8rem",
                            },
                        ),
                        dcc.RadioItems(
                            id="heatmap-attribute-radio",
                            options=[
                                {"label": "Age Group", "value": "age_bin"},
                                {"label": "Length of Stay", "value": "length_of_stay"},
                            ],
                            value="age_bin",
                            className="custom-radio",
                            inline=True,
                        ),
                    ],
                    className="heatmap-filters-container",
                ),
            ],
            className="graph-card-header",
        ),
        # 2x2 Grid of Heatmaps - one for each service
        html.Div(
            [
                dcc.Graph(
                    id="heatmap-emergency",
                    figure=create_heatmap(*get_heatmap_data("age_bin", "emergency"), "Emergency"),
                    config={"responsive": True},
                ),
                dcc.Graph(
                    id="heatmap-icu",
                    figure=create_heatmap(*get_heatmap_data("age_bin", "ICU"), "ICU"),
                    config={"responsive": True},
                ),
                dcc.Graph(
                    id="heatmap-surgery",
                    figure=create_heatmap(*get_heatmap_data("age_bin", "surgery"), "Surgery"),
                    config={"responsive": True},
                ),
                dcc.Graph(
                    id="heatmap-general-medicine",
                    figure=create_heatmap(*get_heatmap_data("age_bin", "general_medicine"), "General Medicine"),
                    config={"responsive": True},
                ),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gridTemplateRows": "1fr 1fr",
                "gap": "10px",
                "flex": "1",
            },
        ),
    ],
    className="graph-card",
    style={"height": "100%", "display": "flex", "flexDirection": "column"},
)


VIOLIN_CHART_CONTAINER = html.Div(
    [
        html.Div(
            [
                html.H3("Distribution Analysis - Violin Chart"),
                html.P("Value distribution across categories with box plot overlay"),
            ]
        ),
        html.Div(
            [
                html.Label("Metric:", style={"color": MAIN_COLORS["text_secondary"], "marginRight": "15px"}),
                dcc.RadioItems(
                    id="violin-metric-radio",
                    options=[
                        {
                            "label": "Patient Satisfaction",
                            "value": "satisfaction_from_patients",
                        },
                        {"label": "Staff Morale", "value": "staff_morale"},
                        {"label": "Refused/Admitted Ratio", "value": "ratio"},
                    ],
                    value="satisfaction_from_patients",
                    inline=True,
                    style={"color": MAIN_COLORS["text"]},
                    inputStyle={"marginRight": "5px", "marginLeft": "15px"},
                    labelStyle={"display": "flex", "alignItems": "center"},
                ),
            ],
            style={"marginBottom": "20px", "display": "flex", "alignItems": "center"},
        ),
        dcc.Graph(
            id="violin-chart",
            figure=create_violin_chart(SERVICES_DATA),
            config={"responsive": False},
            style={"height": "400px"},
        ),
    ],
    className="graph-card",
)


LAYOUT = html.Div(
    [
        # Header
        html.Div(
            [
                html.H1("Data Analysis & Visualization Dashboard"),
                html.P("Explore interactive visualizations with real-time data insights"),
            ],
            className="dashboard-header",
        ),
        dcc.Store(id="global-week-store"),
        # Main Container
        html.Div(
            [
                # Row 1: Stream Graph (Full Width)
                LINECHART_CARD,
                # Row 2: Scatter Plot + Heatmaps (Side by Side)
                html.Div(
                    [
                        SCATTER_PLOT_CARD,
                        HEATMAPS_CONTAINER,
                    ],
                    # Using inline grid styles to enforce a 1:1 split
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                        "marginBottom": "24px",
                        "alignItems": "stretch",
                    },
                ),
                # Row 3: Violin Chart (Full Width)
                VIOLIN_CHART_CONTAINER,
            ],
            className="main-container",
        ),
        # Footer
        html.Div(
            [
                html.P(
                    [
                        "Data Visualization Project - Group 65 | Built with ",
                        html.A(
                            "Dash & Plotly",
                            href="https://plotly.com/dash/",
                            target="_blank",
                        ),
                    ]
                )
            ],
            className="dashboard-footer",
        ),
    ],
    style={"backgroundColor": MAIN_COLORS["bg"], "minHeight": "100vh"},
)
