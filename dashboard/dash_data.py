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
SERVICES = list(SERVICES_MAPPING.keys())
STREAM_DATA = pd.DataFrame(
    {
        "Week": WEEKS * len(SERVICES),
        "Date": DATES * len(SERVICES),
        "Category": np.repeat(SERVICES, 52),
        "Patient Satisfaction": np.concatenate(
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
        "Staff Morale": np.concatenate(
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
        "Available Beds": np.concatenate(
            [
                SERVICES_DATA[SERVICES_DATA["service"] == "emergency"]["available_beds"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "ICU"]["available_beds"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "surgery"]["available_beds"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "general_medicine"]["available_beds"].tolist(),
            ]
        ),
        "Patient Requests": np.concatenate(
            [
                SERVICES_DATA[SERVICES_DATA["service"] == "emergency"]["patients_request"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "ICU"]["patients_request"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "surgery"]["patients_request"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "general_medicine"]["patients_request"].tolist(),
            ]
        ),
        "Patient Admissions": np.concatenate(
            [
                SERVICES_DATA[SERVICES_DATA["service"] == "emergency"]["patients_admitted"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "ICU"]["patients_admitted"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "surgery"]["patients_admitted"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "general_medicine"]["patients_admitted"].tolist(),
            ]
        ),
        "Patient Refusals": np.concatenate(
            [
                SERVICES_DATA[SERVICES_DATA["service"] == "emergency"]["patients_refused"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "ICU"]["patients_refused"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "surgery"]["patients_refused"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "general_medicine"]["patients_refused"].tolist(),
            ]
        ),
        "event": np.concatenate(
            [
                SERVICES_DATA[SERVICES_DATA["service"] == "emergency"]["event"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "ICU"]["event"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "surgery"]["event"].tolist(),
                SERVICES_DATA[SERVICES_DATA["service"] == "general_medicine"]["event"].tolist(),
            ]
        ),
    }
)

# Scatter Plot Data

SCATTER_DATA = SERVICES_DATA.copy()

SCATTER_DATA["Category"] = SCATTER_DATA["service"].map(SERVICES_MAPPING)

SCATTER_DATA["Refused/Admitted Ratio"] = SCATTER_DATA["patients_refused"] / SCATTER_DATA["patients_admitted"].replace(
    0, 1
)

total_staff = SCATTER_DATA["doctors_count"] + SCATTER_DATA["nurses_count"]
SCATTER_DATA["Staff/Patient Ratio"] = total_staff / SCATTER_DATA["patients_admitted"].replace(0, 1)

SCATTER_DATA.rename(
    columns={
        "satisfaction_from_patients": "Satisfaction",
        "staff_morale": "Morale",
        "week": "Week",
    },
    inplace=True,
)

# Select only the columns needed for the Scatter Plot Matrix
SCATTER_DATA = SCATTER_DATA[
    [
        "Week",
        "Category",
        "Satisfaction",
        "Morale",
        "Refused/Admitted Ratio",
        "Staff/Patient Ratio",
        "event",
    ]
]


# Heatmap Data - Real Patient Data
# Labels for heatmap axes
SATISFACTION_BINS = ["60-70", "70-80", "80-90", "90-100"]
AGE_BINS = [
    "0-10",
    "10-20",
    "20-30",
    "30-40",
    "40-50",
    "50-60",
    "60-70",
    "70-80",
    "80-90",
]
LENGTH_OF_STAY_BINS = list(range(1, 15))  # 1 to 14 days


def get_heatmap_data(row_attribute="age_bin", service_filter=None, week_range=None):
    """
    Create a crosstab (patient count matrix) for heatmap visualization.

    Args:
        row_attribute: "age_bin" or "length_of_stay" - what to show on Y-axis
        service_filter: None for all, single service name, or list of services
        week_range: Optional tuple (min_week, max_week) to filter by weeks

    Returns:
        tuple: (z_values, x_labels, y_labels)
    """
    df_show = PATIENTS_DATA

    # Apply week range filter if specified
    if week_range is not None:
        min_week, max_week = week_range
        df_show = df_show[(df_show["week"] >= min_week) & (df_show["week"] <= max_week)]

    # Apply service filter if specified
    if service_filter is not None:
        if isinstance(service_filter, str):
            df_show = df_show[df_show["service"] == service_filter]
        elif isinstance(service_filter, list) and len(service_filter) > 0:
            df_show = df_show[df_show["service"].isin(service_filter)]

    # Create crosstab (count of patients in each cell)
    if row_attribute == "age_bin":
        crosstab = pd.crosstab(df_show["age_bin"], df_show["satisfaction_bin"])
        # Ensure all bins are present and in correct order
        crosstab = crosstab.reindex(index=AGE_BINS, columns=SATISFACTION_BINS, fill_value=0)
        y_labels = AGE_BINS
    else:  # length_of_stay
        crosstab = pd.crosstab(df_show["length_of_stay"], df_show["satisfaction_bin"])
        # Insert a zero-row for a length of stay of 0 (not in LENGTH_OF_STAY_BINS)
        full_index = [0] + LENGTH_OF_STAY_BINS
        crosstab = crosstab.reindex(index=full_index, columns=SATISFACTION_BINS, fill_value=0)
        y_labels = [str(d) for d in full_index]

    z_values = crosstab.values.tolist()
    x_labels = SATISFACTION_BINS

    return z_values, x_labels, y_labels


# Violin Chart Data

VIOLIN_DATA = SERVICES_DATA.copy()

EVENTS = ["Donation", "Flu", "Strike", "None"]
EVENT_MAP = {"donation": 0, "flu": 1, "strike": 2, "none": 3}
METRIC_DISPLAY_NAME = {
    "satisfaction_from_patients": "Patient Satisfaction",
    "staff_morale": "Staff Morale",
    "ratio": "Refused/Admitted Ratio",
}
VIOLIN_DATA["ratio"] = VIOLIN_DATA["patients_refused"] / VIOLIN_DATA["patients_admitted"].replace(0, 1)
