# ============================================
# COLOR SCHEMES - HOSPITAL PROFESSIONAL LIGHT THEME
# Clean, clinical, and visually appealing
# ============================================

MAIN_COLORS = {
    "bg": "#f0f4f8",  # Soft blue-gray background
    "card_bg": "#ffffff",
    "text": "#1e3a5f",  # Deep navy for readability
    "text_secondary": "#4a6fa5",  # Medium blue-gray
    "text_muted": "#7b9bc0",  # Light blue-gray
    "accent": "#0077b6",  # Healthcare blue
    "grid": "rgba(30, 58, 95, 0.1)",
    "highlight": "#e63946",  # Alert red
    "transparent": "rgba(0,0,0,0)",
    "border": "#d0dce8",  # Soft blue-gray border
}

# Professional healthcare color palette - distinct colors for line charts
CHART_COLORS = ["#e63946", "#2a9d8f", "#0077b6", "#f77f00", "#9b5de5"]  # Red, Green, Blue, Orange, Purple
STREAM_GRAPH_COLORS = ["#e63946", "#0077b6", "#2a9d8f", "#f77f00", "#f0f4f8"]

# Heatmap: Light lavender to deep indigo (darker = more patients)
HEATMAP_COLORSCALE = [
    [0, "#f8f9fa"],      # Almost white for zero
    [0.2, "#e0e7ff"],    # Very light indigo
    [0.4, "#a5b4fc"],    # Light indigo
    [0.6, "#6366f1"],    # Medium indigo
    [0.8, "#4338ca"],    # Dark indigo
    [1, "#312e81"]       # Very dark indigo
]

# Event colors for violin chart
EVENT_COLORS = {
    "flu": "#e63946",
    "strike": "#f77f00",
    "donation": "#2a9d8f",
    "none": "#0077b6",
    "unknown": "#6366f1",
}

# Violin chart specific colors
VIOLIN_CHART_COLORS = {
    "default_service": "#0077b6",
    "aggregated_none": "#0077b6",
    "opacity": 0.7,
}


# ============================================
# PLOTLY FIGURE TEMPLATE
# ============================================

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "#ffffff",
        "plot_bgcolor": "#ffffff",
        "font": {"color": MAIN_COLORS["text"], "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": MAIN_COLORS["grid"],
            "zerolinecolor": MAIN_COLORS["grid"],
            "tickfont": {"color": MAIN_COLORS["text_secondary"]},
            "linecolor": MAIN_COLORS["border"],
            "linewidth": 1,
        },
        "yaxis": {
            "gridcolor": MAIN_COLORS["grid"],
            "zerolinecolor": MAIN_COLORS["grid"],
            "tickfont": {"color": MAIN_COLORS["text_secondary"]},
            "linecolor": MAIN_COLORS["border"],
            "linewidth": 1,
        },
        "colorway": CHART_COLORS,
        "hoverlabel": {
            "bgcolor": "#ffffff",
            "font": {"color": MAIN_COLORS["text"], "family": "Inter"},
            "bordercolor": MAIN_COLORS["border"],
        },
    }
}
