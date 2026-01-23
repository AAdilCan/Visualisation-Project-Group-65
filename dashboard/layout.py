from dash import dcc, html
import dash_bootstrap_components as dbc

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

# =========================================
# 1. FLOATING FILTER BUTTON (TOP LEFT)
# =========================================
FILTER_BUTTON = html.Button(
    "⚙️ Filters",
    id="filter-button",
    n_clicks=0,
    style={
        "position": "fixed",
        "top": "30px",
        "left": "30px",
        "zIndex": "1050",
        "padding": "10px 20px",
        "backgroundColor": MAIN_COLORS["accent"],
        "color": "white",
        "border": "none",
        "borderRadius": "50px",
        "boxShadow": "0 4px 12px rgba(0,0,0,0.3)",
        "fontSize": "1rem",
        "cursor": "pointer",
        "fontWeight": "bold",
    },
)

# =========================================
# 2. OVERLAY SIDEBAR (Services Only)
# =========================================
SIDEBAR_OVERLAY = html.Div(
    [
        # --- Header with Close Button ---
        html.Div(
            [
                html.H3("Dashboard Filters", style={"margin": "0"}),
                html.Button(
                    "✕",
                    id="close-sidebar",
                    n_clicks=0,
                    style={
                        "background": "none",
                        "border": "none",
                        "fontSize": "1.5rem",
                        "cursor": "pointer",
                        "color": MAIN_COLORS["text_secondary"]
                    }
                )
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "marginBottom": "20px",
                "borderBottom": f"1px solid {MAIN_COLORS['grid']}",
                "paddingBottom": "10px"
            }
        ),

        # --- Filters ---
        html.Label("Select Services:", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
        dcc.Checklist(
            id="services-checklist",
            options=[{"label": label, "value": service} for service, label in SERVICES_MAPPING.items()],
            value=[SERVICES[0]],
            className="custom-checklist",
            style={"display": "flex", "flexDirection": "column", "gap": "8px", "marginBottom": "25px"}
        ),

        # NOTE: Metric checklist removed from here

        html.Div(
            "ℹ️ These filters update all charts.",
            style={"marginTop": "auto", "fontSize": "0.85rem", "color": MAIN_COLORS["text_muted"]}
        )
    ],
    id="sidebar-overlay",
    style={
        "position": "fixed",
        "top": "0",
        "left": "-350px",
        "width": "300px",
        "height": "100vh",
        "backgroundColor": "white",
        "boxShadow": "5px 0 15px rgba(0,0,0,0.2)",
        "padding": "30px",
        "zIndex": "1100",
        "transition": "left 0.3s ease-in-out",
        "overflowY": "auto"
    },
)

# =========================================
# 3. LINECHART (Metrics Added Here)
# =========================================

LINECHART_CARD = html.Div(
    [
        html.Div(
            [
                # LEFT: Title & Info
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "Services Weekly Performance",
                                    style={"display": "inline-block", "marginRight": "10px", "marginBottom": "0"}
                                ),
                                html.Span(
                                    "| Satisfaction & Morale vs Patient Distribution",
                                    style={"color": MAIN_COLORS["text_secondary"], "fontSize": "0.9rem"}
                                ),
                            ],
                            style={"marginBottom": "4px"}
                        ),
                        html.P(
                            "* Streamgraph scale differs from metrics. Services selection applies globally.",
                            style={
                                "color": MAIN_COLORS["text_muted"],
                                "fontSize": "0.75rem",
                                "fontStyle": "italic",
                                "margin": "0"
                            },
                        ),
                    ],
                    style={"flex": "1"}
                ),

                # RIGHT: Metrics Filter Box
                html.Div(
                    [
                        html.Label(
                            "Metrics:",
                            style={
                                "fontWeight": "bold",
                                "fontSize": "0.85rem",
                                "marginRight": "10px",
                                "color": MAIN_COLORS["text"]
                            }
                        ),
                        dcc.Checklist(
                            id="metric-checklist",
                            options=[
                                {"label": "Patient Satisfaction", "value": "Patient Satisfaction"},
                                {"label": "Staff Morale", "value": "Staff Morale"},
                            ],
                            value=["Patient Satisfaction"],
                            className="custom-checklist",
                            inline=True,  # Display horizontally
                            inputStyle={"marginRight": "5px", "cursor": "pointer"},
                            labelStyle={"marginRight": "15px", "display": "inline-flex", "alignItems": "center",
                                        "cursor": "pointer"}
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "backgroundColor": "rgba(0, 0, 0, 0.05)",
                        "padding": "8px 15px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
                    }
                )
            ],
            className="graph-card-header",
            # Added display:flex to justify content (Title Left, Filter Right)
            style={
                "paddingLeft": "120px",
                "paddingTop": "15px",
                "paddingBottom": "10px",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "flexWrap": "wrap",
                "gap": "15px"
            }
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


# =========================================
# 4. SCATTERPLOT MATRIX
# =========================================

SCATTER_PLOT_CARD = html.Div(
    [
        # Header Container
        html.Div(
            [
                # LEFT: Title
                html.Div(
                    [
                        html.H3("Scatter Plot Analysis", style={"margin": "10"}),
                        html.P("Correlation Matrix of Service Metrics", style={"margin": "0"}),
                    ],
                    style={"flex": "1", "paddingLeft": "15px"}  # Added padding as requested
                ),

            ],
            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "10px",
                   "paddingTop": "10px"}
        ),

        dcc.Graph(
            id="scatter-plot",
            figure=create_scatter_plot(),
            config={"responsive": True},
            style={"height": "800px"},
        ),
    ],
    className="graph-card",
    style={"height": "100%", "padding": "10px"},
)

# =========================================
# 5. HEATMAP
# =========================================

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
        dcc.Graph(
            id="heatmap-main",
            figure=create_heatmap(*get_heatmap_data("age_bin", None), "Age Group vs Patient Satisfaction"),
            config={"responsive": True},
            style={"flex": "1"},
        ),
    ],
    className="graph-card",
    style={"height": "100%", "display": "flex", "flexDirection": "column"},
)


# =========================================
# 6. VIOLIN CHART
# =========================================

VIOLIN_CHART_CONTAINER = html.Div(
    [
        html.Div(
            [
                # LEFT: Text Info
                html.Div(
                    [
                        html.H3("Distribution Analysis - Violin Chart", style={"marginTop": "0"}),
                        html.P(
                            "Value distribution across categories with box plot overlay",
                            style={"marginBottom": "0"}
                        ),
                    ],
                    style={"flex": "1"}
                ),

                # RIGHT: Boxed Controls
                html.Div(
                    [
                        html.Label(
                            "Select Metric:",
                            style={
                                "color": MAIN_COLORS["text"],
                                "fontWeight": "bold",
                                "marginBottom": "5px",
                                "display": "block",
                                "fontSize": "0.85rem"
                            }
                        ),
                        dcc.RadioItems(
                            id="violin-metric-radio",
                            options=[
                                {"label": "Patient Satisfaction", "value": "satisfaction_from_patients"},
                                {"label": "Staff Morale", "value": "staff_morale"},
                                {"label": "Refused/Admitted Ratio", "value": "ratio"},
                            ],
                            value="satisfaction_from_patients",
                            inline=True,
                            className="custom-radio",
                            inputStyle={"marginRight": "5px", "cursor": "pointer"},
                            labelStyle={"marginRight": "15px", "display": "inline-flex", "alignItems": "center",
                                        "cursor": "pointer"}
                        ),

                    ],
                    # Styling the container box
                    style={
                        "backgroundColor": "rgba(0, 0, 0, 0.05)",
                        "padding": "10px 15px",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 5px rgba(0,0,0,0.1)",
                        "minWidth": "300px"
                    }
                ),
            ],
            # Header Container Styles
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "flexWrap": "wrap",
                "gap": "15px",
                "marginBottom": "15px"
            }
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


# =========================================
# 7. LAYOUT
# =========================================

LAYOUT = html.Div(
    [
        FILTER_BUTTON,
        SIDEBAR_OVERLAY,
        # Header
        html.Div(
            [
                html.H1("Data Analysis & Visualization Dashboard"),
                html.P("Explore interactive visualizations with real-time data insights"),
            ],
            className="dashboard-header",
            # Add padding top/left to avoid overlap with fixed button
            style={"paddingLeft": "80px", "paddingTop": "10px"}
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