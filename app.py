# Interactive Data Visualization Dashboard
# Featuring: Stream Graph, Scatter Plot, Heatmaps, and Violin Chart

import dash

from dashboard.layout import LAYOUT
import dashboard.callbacks  # noqa: F401, Import callbacks to register them


# ============================================
# INITIALIZE DASH APP
# ===========================================

app = dash.Dash(
    __name__,
    title="Data Visualization Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.layout = LAYOUT

if __name__ == "__main__":
    app.run(debug=True, port=8050)
