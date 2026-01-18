# ============================================
# COLOR SCHEMES
# ============================================

MAIN_COLORS = {
    "bg": "#0f0f1a",
    "card_bg": "rgba(30, 30, 50, 0.8)",
    "text": "#ffffff",
    "text_secondary": "#a0a0b0",
    "text_muted": "#6b7280",
    "accent": "#6366f1",
    "grid": "rgba(255, 255, 255, 0.1)",
    "highlight": "#ff6464",
    "transparent": "rgba(0,0,0,0)",
}

# Vibrant color palette for charts
CHART_COLORS = ["#6366f1", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b"]
STREAM_GRAPH_COLORS = ["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#0f0f1a"]
HEATMAP_COLORSCALE = [[0, "#1e1e3c"], [0.25, "#3b3b6d"], [0.5, "#6366f1"], [0.75, "#8b5cf6"], [1, "#c4b5fd"]]

# Event colors for violin chart (maps to specific events)
EVENT_COLORS = {
    "flu": "#ef4444",
    "strike": "#f59e0b",
    "donation": "#10b981",
    "none": "#6366f1",
    "unknown": "#8b5cf6",
}


# ============================================
# PLOTLY FIGURE TEMPLATE
# ============================================

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": MAIN_COLORS["text"], "family": "Inter, sans-serif"},
        "xaxis": {
            "gridcolor": MAIN_COLORS["grid"],
            "zerolinecolor": MAIN_COLORS["grid"],
            "tickfont": {"color": MAIN_COLORS["text_secondary"]},
        },
        "yaxis": {
            "gridcolor": MAIN_COLORS["grid"],
            "zerolinecolor": MAIN_COLORS["grid"],
            "tickfont": {"color": MAIN_COLORS["text_secondary"]},
        },
        "colorway": CHART_COLORS,
        "hoverlabel": {"bgcolor": MAIN_COLORS["card_bg"], "font": {"color": MAIN_COLORS["text"], "family": "Inter"}},
    }
}
