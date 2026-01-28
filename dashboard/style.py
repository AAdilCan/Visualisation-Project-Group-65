# ============================================
# COLOR SCHEMES - CLINICAL LIGHT THEME (V2)
# ============================================

MAIN_COLORS = {
    "bg": "#f8fafc",
    "card_bg": "#ffffff",
    "text": "#1e293b",
    "text_secondary": "#475569",
    "text_muted": "#94a3b8",
    "accent": "#2563eb",
    "grid": "#e2e8f0",
    "highlight": "#ef4444",
    "transparent": "rgba(0,0,0,0)",
    "border": "#d0dce8",  # Soft blue-gray border
}

# Requested Services Palette: Blue, Green, Yellow, Red, Indigo
CHART_COLORS = ["#2563eb", "#10b981", "#f59e0b", "#ef4444", "#6366f1"]

STREAM_GRAPH_COLORS = [
    "#2563eb",  # Darker Blue (Available Beds)
    "#93c5fd",  # Light Blue (Patient Requests
    "#86efac",  # Light Green (Patient Admissions)
    "#fda4af",  # Light Red (Patient Refusals)
    "#f8fafc",  # Background Match
]

# Standard "YlGnBu" (Yellow-Green-Blue) Heatmap for high visibility
HEATMAP_COLORSCALE = [
    [0.0, "#f8fafc"],  # Matches your MAIN_COLORS['bg'] for zero/low values
    [0.1, "#e0f2fe"],  # Lightest sky blue
    [0.3, "#7dd3fc"],  # Soft medical blue
    [0.5, "#3b82f6"],  # Vibrant accent blue
    [0.7, "#1d4ed8"],  # Deep primary blue
    [1.0, "#1e3a8a"],  # Navy indigo for peak values
]

EVENT_COLORS = {
    "flu": "#ef4444",  # Red
    "strike": "#f59e0b",  # Yellow/Orange
    "donation": "#10b981",  # Green
    "none": "#2563eb",  # Blue
    "unknown": "#94a3b8",
}

VIOLIN_CHART_COLORS = {
    "default_service": "#2563eb",
    "aggregated_none": "#cbd5e1",
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
            "showline": True,
            "linecolor": MAIN_COLORS["grid"],
        },
        "yaxis": {
            "gridcolor": MAIN_COLORS["grid"],
            "zerolinecolor": MAIN_COLORS["grid"],
            "tickfont": {"color": MAIN_COLORS["text_secondary"]},
            "showline": True,
            "linecolor": MAIN_COLORS["grid"],
        },
        "colorway": CHART_COLORS,
        "hoverlabel": {
            "bgcolor": "#ffffff",
            "font": {"color": MAIN_COLORS["text"], "family": "Inter"},
            "bordercolor": MAIN_COLORS["grid"],
        },
    }
}
