# HospiTools: Interactive Hospital Data Visualization Dashboard

## Overview
**HospiTools** applies interactive visualization techniques to explore hospital service performance, focusing on patient satisfaction, staff morale, and resource allocation. The dashboard provides clear, actionable insights through interconnected views, following Munzner's rigorous design principles.

## How to Run the Tool

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation
1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/YourUsername/Visualisation-Project-Group-65.git
    cd Visualisation-Project-Group-65
    ```

2.  **Install dependencies**:
    Create a virtual environment (recommended) and install the required packages:
    ```bash
    # Create virtual environment (optional but recommended)
    python -m venv venv
    # Activate virtual environment
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate

    # Install requirements
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    Execute the main application script:
    ```bash
    python app.py
    ```

4.  **Access the Dashboard**:
    Open your web browser and navigate to:
    `http://127.0.0.1:8050/`

## Implementation Details

This project distinguishes between custom implementation logic and external libraries as follows:

### Self-Implemented Code
The core logic, data transformation, and UI design were implemented by the team:
-   **Dashboard Layout (`dashboard/layout.py`)**: Designed the entire grid system, sidebar navigation, and component placement.
-   **Interactivity & Callbacks (`dashboard/callbacks.py`)**: Wrote all callback functions to handle user interactions (filtering, cross-filtering linked views, updating graphs dynamically).
-   **Data Processing (`dashboard/dash_data.py`)**: Implemented data loading, cleaning, and transformation logic to prepare datasets for visualization.
-   **Custom Styling (`assets/styles.css`)**: Created custom CSS for the floating action button, sidebar transitions, card layouts, and typography overrides to achieve a polished look beyond default Dash styles.
-   **Visualization Logic**:
    -   **Stream Graph (`dashboard/linechart.py`)**: Custom implementation using Plotly graph objects to simulate a stream graph effect.
    -   **Scatter Plot Matrix (`dashboard/scatterplot_matrix.py`)**: Configured the SPLOM (Scatter Plot Matrix) with custom dimensions and interactivity.
    -   **Heatmaps (`dashboard/heatmap.py`)**: Built the logic to generate multiple heatmaps dynamically based on selected attributes (Age vs. Length of Stay).
    -   **Violin Chart (`dashboard/violinchart.py`)**: Implemented the violin plot with box plot overlays for distribution analysis.

### External Libraries & Resources
We leveraged the following open-source libraries and resources:
-   **Dash (by Plotly)**: used as the main web application framework.
-   **Plotly Graph Objects & Express**: Used as the plotting engine for all charts.
-   **Pandas**: Used for efficient data manipulation and aggregation.
-   **NumPy**: Used for numerical operations and generating synthetic data distributions where needed.
-   **Google Fonts**: The "Inter" font family is loaded via external CSS for typography.
