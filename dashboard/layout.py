from dash import dcc, html

from dashboard.dash_data import get_heatmap_data, SERVICES, SERVICES_MAPPING, SERVICES_DATA
from dashboard.heatmap import create_heatmap
from dashboard.linechart import create_line_chart
from dashboard.scatterplot_matrix import create_scatter_plot
from dashboard.violinchart import create_violin_chart

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
                                "color": "#6b7280",
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
                            "Metrics:",
                            style={
                                "color": "#a0a0b0",
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
                        html.Label(
                            "Services:",
                            style={
                                "color": "#a0a0b0",
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
    style={"height": "100%"}
)


HEATMAPS_CONTAINER = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Patient Satisfaction Heatmap"),
                        html.P("Distribution of patients across satisfaction levels"),
                    ],
                    style={"flex": "1"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Group By:",
                            style={
                                "color": "#a0a0b0",
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
                        html.Label(
                            "Service:",
                            style={
                                "color": "#a0a0b0",
                                "marginBottom": "8px",
                                "marginTop": "12px",
                                "display": "block",
                                "fontSize": "0.8rem",
                            },
                        ),
                        dcc.Dropdown(
                            id="heatmap-service-dropdown",
                            options=[
                                {"label": "All Services", "value": "all"},
                            ] + [
                                {"label": label, "value": service}
                                for service, label in SERVICES_MAPPING.items()
                            ],
                            value="all",
                            clearable=False,
                            style={
                                "width": "180px",
                                "backgroundColor": "#1a1a2e",
                                "color": "#ffffff",
                            },
                        ),
                    ],
                    className="heatmap-filters-container",
                ),
            ],
            className="graph-card-header",
        ),
        dcc.Graph(
            id="heatmap-main",
            figure=create_heatmap(
                *get_heatmap_data("age_bin", None),
                "Age Group vs Patient Satisfaction"
            ),
            config={"responsive": False},
            style={"height": "500px"},
        ),
    ],
    className="graph-card",
    style={"height": "100%"}
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
                html.Label("Filter by Quarter:", style={"color": "#a0a0b0", "marginRight": "15px"}),
                dcc.Dropdown(
                    id="quarter-dropdown",
                    options=[
                        {"label": "All Quarters", "value": "all"},
                        {"label": "Q1", "value": "Q1"},
                        {"label": "Q2", "value": "Q2"},
                        {"label": "Q3", "value": "Q3"},
                        {"label": "Q4", "value": "Q4"},
                    ],
                    value="all",
                    clearable=False,
                    style={"width": "200px", "backgroundColor": "#1a1a2e", "color": "#ffffff"},
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
                        "alignItems": "start"
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
                        html.A("Dash & Plotly", href="https://plotly.com/dash/", target="_blank"),
                    ]
                )
            ],
            className="dashboard-footer",
        ),
    ],
    style={"backgroundColor": "#0f0f1a", "minHeight": "100vh"},
)