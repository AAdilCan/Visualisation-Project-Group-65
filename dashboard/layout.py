from dash import dcc, html

from dashboard.dash_data import HEATMAP1, HEATMAP2, HEATMAP3, HEATMAP4
from dashboard.heatmap import create_heatmap
from dashboard.linechart import create_line_chart
from dashboard.scatterplot_matrix import create_scatter_plot
from dashboard.violinchart import create_violin_chart


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
                # Top Row: Stream Graph + Scatter Plot
                html.Div(
                    [
                        # Main Stream Graph Card
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H3("Stream Graph with Trend Analysis"),
                                                html.P("Category performance over time with average trend"),
                                            ],
                                            style={"flex": "1"},
                                        ),
                                        html.Div(
                                            [
                                                html.Label(
                                                    "Select Metrics:",
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
                                                            "label": " Patient Satisfaction",
                                                            "value": "patient_satisfaction",
                                                        },
                                                        {"label": " Staff Morale", "value": "staff_morale"},
                                                    ],
                                                    value=["patient_satisfaction"],
                                                    className="custom-checklist",
                                                ),
                                            ],
                                            className="metric-controls-container",
                                        ),
                                    ],
                                    className="graph-card-header",
                                ),
                                dcc.Graph(
                                    id="stream-graph",
                                    figure=create_line_chart(["patient_satisfaction"]),
                                    config={"responsive": False},
                                    style={"height": "500px"},
                                ),
                            ],
                            className="graph-card",
                        ),
                        # Scatter Plot Card
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3("Scatter Plot Analysis"),
                                        html.P("Correlation between variables by category"),
                                    ]
                                ),
                                dcc.Graph(
                                    id="scatter-plot",
                                    figure=create_scatter_plot(),
                                    config={"responsive": False},
                                    style={"height": "450px"},
                                ),
                            ],
                            className="graph-card",
                        ),
                    ],
                    className="top-row",
                ),
                # Heatmaps Section
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Correlation Heatmaps"),
                                html.P("Four correlation matrices showing relationships between variables"),
                            ]
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="heatmap-1",
                                            figure=create_heatmap(HEATMAP1, "Dataset A"),
                                            config={"responsive": False},
                                            style={"height": "250px"},
                                        )
                                    ],
                                    className="heatmap-card",
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="heatmap-2",
                                            figure=create_heatmap(HEATMAP2, "Dataset B"),
                                            config={"responsive": False},
                                            style={"height": "250px"},
                                        )
                                    ],
                                    className="heatmap-card",
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="heatmap-3",
                                            figure=create_heatmap(HEATMAP3, "Dataset C"),
                                            config={"responsive": False},
                                            style={"height": "250px"},
                                        )
                                    ],
                                    className="heatmap-card",
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="heatmap-4",
                                            figure=create_heatmap(HEATMAP4, "Dataset D"),
                                            config={"responsive": False},
                                            style={"height": "250px"},
                                        )
                                    ],
                                    className="heatmap-card",
                                ),
                            ],
                            className="heatmaps-container",
                        ),
                    ],
                    className="graph-card",
                ),
                # Violin Chart Section
                html.Div(
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
                            figure=create_violin_chart(),
                            config={"responsive": False},
                            style={"height": "400px"},
                        ),
                    ],
                    className="graph-card",
                ),
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
