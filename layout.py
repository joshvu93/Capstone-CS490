"""Widget construction for the MiceLab workflow."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)


def create_import_section():
    section = QGroupBox("1. Import tracking data")
    layout = QGridLayout(section)
    dorsal_button, lateral_button = QPushButton("Choose dorsal CSV"), QPushButton(
        "Choose lateral CSV"
    )
    dorsal_status, lateral_status = QLabel("No dorsal file selected"), QLabel(
        "No lateral file selected"
    )
    layout.addWidget(dorsal_button, 0, 0)
    layout.addWidget(dorsal_status, 0, 1)
    layout.addWidget(lateral_button, 1, 0)
    layout.addWidget(lateral_status, 1, 1)
    return {
        "section": section,
        "dorsal_button": dorsal_button,
        "dorsal_status": dorsal_status,
        "lateral_button": lateral_button,
        "lateral_status": lateral_status,
    }


def create_parameter_section():
    section = QGroupBox("2. Calibration and processing parameters")
    layout = QGridLayout(section)
    fps = QSpinBox()
    fps.setRange(1, 10000)
    fps.setValue(250)
    fps.setSuffix(" fps")
    latcal = QDoubleSpinBox()
    latcal.setDecimals(8)
    latcal.setRange(0.00000001, 1)
    latcal.setValue(0.00026895)
    latcal.setSuffix(" m/px")
    dorscal = QDoubleSpinBox()
    dorscal.setDecimals(8)
    dorscal.setRange(0.00000001, 1)
    dorscal.setValue(0.00027257)
    dorscal.setSuffix(" m/px")
    order = QSpinBox()
    order.setRange(0, 8)
    order.setValue(2)
    threshold = QDoubleSpinBox()
    threshold.setDecimals(2)
    threshold.setRange(0, 1)
    threshold.setSingleStep(0.05)
    threshold.setValue(0.2)
    smooth = QDoubleSpinBox()
    smooth.setDecimals(3)
    smooth.setRange(0.004, 2)
    smooth.setSingleStep(0.01)
    smooth.setValue(0.04)
    smooth.setSuffix(" s")
    tail_diameter = QDoubleSpinBox()
    tail_diameter.setDecimals(6)
    tail_diameter.setRange(0.000001, 1)
    tail_diameter.setSingleStep(0.0001)
    tail_diameter.setValue(0.00225)
    tail_diameter.setSuffix(" m")
    fields = [
        ("Frame rate", fps),
        ("Lateral calibration", latcal),
        ("Dorsal calibration", dorscal),
        ("Detrend polynomial order", order),
        ("Minimum DLC likelihood", threshold),
        ("Smoothing window", smooth),
        ("Tail diameter", tail_diameter),
    ]
    for row, (label, widget) in enumerate(fields):
        layout.addWidget(QLabel(label), row // 2, (row % 2) * 2)
        layout.addWidget(widget, row // 2, (row % 2) * 2 + 1)
    return {
        "section": section,
        "fps_input": fps,
        "latcal_input": latcal,
        "dorscal_input": dorscal,
        "poly1_input": order,
        "poly2_input": threshold,
        "poly3_input": smooth,
        "td_input": tail_diameter,
        "parameter_button": QPushButton("Apply parameters"),
    }


def create_selection_section():
    section = QGroupBox("3. Inspect data")
    layout = QGridLayout(section)
    view, stage, variable = QComboBox(), QComboBox(), QComboBox()
    manual_edit_button = QPushButton("Manual outlier editing: off")
    manual_edit_button.setCheckable(True)
    undo_button = QPushButton("Undo point")
    clear_button = QPushButton("Clear manual points")
    manual_help = QLabel(
        "Enable editing, then click a sample to mark or restore it as an outlier."
    )
    manual_help.setWordWrap(True)
    stage.addItems(
        [
            "Raw",
            "Filtered",
            "Gap filled",
            "Converted and detrended",
            "Standardized and smoothed",
        ]
    )
    layout.addWidget(QLabel("View"), 0, 0)
    layout.addWidget(view, 0, 1)
    layout.addWidget(QLabel("Workflow stage"), 0, 2)
    layout.addWidget(stage, 0, 3)
    layout.addWidget(QLabel("Coordinate"), 1, 0)
    layout.addWidget(variable, 1, 1, 1, 3)
    layout.addWidget(manual_edit_button, 2, 0)
    layout.addWidget(undo_button, 2, 1)
    layout.addWidget(clear_button, 2, 2)
    layout.addWidget(manual_help, 3, 0, 1, 4)
    return {
        "section": section,
        "dataset_selector": view,
        "stage_selector": stage,
        "variable_selector": variable,
        "manual_edit_button": manual_edit_button,
        "undo_button": undo_button,
        "clear_button": clear_button,
    }


def create_processing_section():
    section = QGroupBox("4. Process data in flowchart order")
    layout = QGridLayout(section)
    buttons = [
        QPushButton(label)
        for label in (
            "5. Filter outliers",
            "6. Fill gaps with spline",
            "7. Convert units & detrend",
            "8. Standardize & smooth",
        )
    ]
    for i, button in enumerate(buttons):
        layout.addWidget(button, i // 2, i % 2)
    return {
        "section": section,
        "filter_button": buttons[0],
        "fill_gap_button": buttons[1],
        "convert_button": buttons[2],
        "smooth_button": buttons[3],
    }


def create_kinematics_section():
    section = QGroupBox("9. Kinematics and results")
    layout = QVBoxLayout(section)
    calculate_button = QPushButton("Calculate tail and hindlimb kinematics")
    results_label = QLabel("Import and process data to calculate kinematics.")
    results_label.setWordWrap(True)
    layout.addWidget(calculate_button, alignment=Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(results_label)
    return {
        "section": section,
        "calculate_button": calculate_button,
        "results_label": results_label,
    }


def create_export_section():
    section = QGroupBox("10. Export")
    layout = QHBoxLayout(section)
    data, results = QPushButton("Save processed CSV"), QPushButton(
        "Save kinematics CSV + overview plot"
    )
    layout.addWidget(data)
    layout.addWidget(results)
    return {
        "section": section,
        "export_data_button": data,
        "export_results_button": results,
    }
