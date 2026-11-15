# evidently_report.py - Evidently monitoring report for Addition API

import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, DataQualityPreset
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
)
import os

# ── Simulate reference and current data for the Addition API ───────────────
# Reference data: typical inputs and outputs seen during development/testing
reference_data = pd.DataFrame({
    "num1":   [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
    "num2":   [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
    "result": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0, 20.0],
})

# Current data: simulated recent API requests (slight variation to trigger drift detection)
current_data = pd.DataFrame({
    "num1":   [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
    "num2":   [5.0,  15.0, 25.0, 35.0, 45.0, 55.0, 65.0, 75.0, 85.0, 95.0],
    "result": [15.0, 35.0, 55.0, 75.0, 95.0, 115.0, 135.0, 155.0, 175.0, 195.0],
})


def generate_report():
    """Generate an Evidently HTML report and save it to reports/."""
    os.makedirs("reports", exist_ok=True)

    report = Report(metrics=[
        DatasetDriftMetric(),
        DataDriftPreset(),
        DataQualityPreset(),
        ColumnDriftMetric(column_name="num1"),
        ColumnDriftMetric(column_name="num2"),
        ColumnDriftMetric(column_name="result"),
    ])

    report.run(reference_data=reference_data, current_data=current_data)

    output_path = "reports/addition_evidently_report.html"
    report.save_html(output_path)
    print(f"[Evidently] Report saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_report()
