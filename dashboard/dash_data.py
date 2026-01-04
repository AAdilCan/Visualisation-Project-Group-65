import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# ============================================
# IMPORT HOSPITAL DATA
# ============================================

SERVICES_DATA = pd.read_csv(Path(__file__).parent.parent / "data" / "df_services_weekly_prepped.csv")
PATIENTS_DATA = pd.read_csv(Path(__file__).parent.parent / "data" / "df_patients_prepped.csv")

# ============================================
# SAMPLE DATA GENERATION
# ============================================

np.random.seed(42)

# Generate date range for 52 weeks
START_DATE = datetime(2025, 1, 1)
DATES = [START_DATE + timedelta(weeks=i) for i in range(52)]
WEEKS = list(range(1, 53))

SERVICES_MAPPING = {
    "emergency": "Emergency",
    "ICU": "ICU",
    "surgery": "Surgery",
    "general_medicine": "General Medicine",
}

# Stream Graph Data (multiple categories over time)
SERVICES = list(SERVICES_MAPPING.values())
STREAM_DATA = pd.DataFrame(
    {
        "Week": WEEKS * len(SERVICES),
        "Date": DATES * len(SERVICES),
        "Category": np.repeat(SERVICES, 52),
        "patient_satisfaction": np.concatenate(
            [
                SERVICES_DATA[SERVICES_DATA["service"] == "emergency"][
                    "satisfaction_from_patients"
                ].tolist(),  # Emergency - upward trend
                SERVICES_DATA[SERVICES_DATA["service"] == "ICU"][
                    "satisfaction_from_patients"
                ].tolist(),  # ICU - moderate growth
                SERVICES_DATA[SERVICES_DATA["service"] == "surgery"][
                    "satisfaction_from_patients"
                ].tolist(),  # Surgery - volatile
                SERVICES_DATA[SERVICES_DATA["service"] == "general_medicine"][
                    "satisfaction_from_patients"
                ].tolist(),  # General Medicine - slight decline
            ]
        ),
        "staff_morale": np.concatenate(
            [
                SERVICES_DATA[SERVICES_DATA["service"] == "emergency"][
                    "staff_morale"
                ].tolist(),  # Emergency - upward trend
                SERVICES_DATA[SERVICES_DATA["service"] == "ICU"]["staff_morale"].tolist(),  # ICU - moderate growth
                SERVICES_DATA[SERVICES_DATA["service"] == "surgery"]["staff_morale"].tolist(),  # Surgery - volatile
                SERVICES_DATA[SERVICES_DATA["service"] == "general_medicine"][
                    "staff_morale"
                ].tolist(),  # General Medicine - slight decline
            ]
        ),
    }
)

# Scatter Plot Data
n_points = 200
SCATTER_DATA = pd.DataFrame(
    {
        "X_Value": np.random.randn(n_points) * 20 + 50,
        "Y_Value": np.random.randn(n_points) * 15 + 40,
        "Size": np.random.uniform(10, 50, n_points),
        "Category": np.random.choice(SERVICES, n_points),
        "Performance": np.random.uniform(0, 100, n_points),
    }
)
SCATTER_DATA["Y_Value"] = SCATTER_DATA["X_Value"] * 0.6 + np.random.randn(n_points) * 10 + 10


# Heatmap Data (4 different correlation matrices)
def generate_heatmap_data(n=8, seed=None):
    if seed:
        np.random.seed(seed)
    data = np.random.randn(100, n)
    corr = np.corrcoef(data.T)
    return corr


HEATMAP1 = generate_heatmap_data(8, 1)
HEATMAP2 = generate_heatmap_data(8, 2)
HEATMAP3 = generate_heatmap_data(8, 3)
HEATMAP4 = generate_heatmap_data(8, 4)

HEATMAP_LABELS = ["A", "B", "C", "D", "E", "F", "G", "H"]

# Violin Chart Data
VIOLIN_DATA = pd.DataFrame(
    {
        "Category": np.repeat(SERVICES, 100),
        "Value": np.concatenate(
            [
                np.random.normal(60, 15, 100),  # Emergency
                np.random.normal(45, 10, 100),  # ICU
                np.random.normal(55, 20, 100),  # Surgery
                np.random.normal(40, 12, 100),  # General Medicine
            ]
        ),
        "Quarter": np.tile(np.repeat(["Q1", "Q2", "Q3", "Q4"], 25), 4),
    }
)
