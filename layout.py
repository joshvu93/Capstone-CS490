# Imports

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QDoubleSpinBox,
)


# ================================================
# Import Data Section
# ================================================


    
def create_import_section():

    section = QGroupBox("1. Input Data")
    layout = QVBoxLayout(section)
    layout.setSpacing(4)

    # Dorsal data
    dorsal_label = QLabel("Dorsal (Top)")
    dorsal_button = QPushButton("Choose Dorsal CSV")
    dorsal_status = QLabel("No dorsal file selected")

    # Lateral data
    lateral_label = QLabel("Lateral (Side)")
    lateral_button = QPushButton("Choose Lateral CSV")
    lateral_status = QLabel("No lateral file selected")

    dorsal_status.setObjectName("file_status")
    lateral_status.setObjectName("file_status")

    # Add widgets to layout
    for label, button, status in (
        (dorsal_label, dorsal_button, dorsal_status),
        (lateral_label, lateral_button, lateral_status),
    ):
        row = QHBoxLayout()
        row.addWidget(label)
        row.addWidget(button, stretch=1)
        layout.addLayout(row)
        layout.addWidget(status)

    return {
        "section": section,
        "dorsal_button": dorsal_button,
        "dorsal_status": dorsal_status,
        "lateral_button": lateral_button,
        "lateral_status": lateral_status
    }



# ================================================
# Parameter Section
# ================================================

def create_parameter_section():


    section = QGroupBox(
        "2. Calibration Parameters"
    )


    layout = QGridLayout(
        section
    )


    layout.setHorizontalSpacing(
        8
    )

    layout.setVerticalSpacing(
        6
    )


    # ============================================
    # FPS
    # ============================================

    fps_label = QLabel(
        "FPS:"
    )

    fps_input = QSpinBox()
    fps_input.setRange(1, 10000)
    fps_input.setSingleStep(1)
    fps_input.setValue(250)



    layout.addWidget(
        fps_label,
        0,
        0
    )

    layout.addWidget(
        fps_input,
        0,
        1
    )


    # ============================================
    # Latcal
    # ============================================

    latcal_label = QLabel(
        "Latcal (m/pix):"
    )

    latcal_input = QDoubleSpinBox()
    latcal_input.setDecimals(8)
    latcal_input.setRange(0.0, 1.0)
    latcal_input.setSingleStep(0.00000001)
    latcal_input.setValue(0.00026895)


    layout.addWidget(
        latcal_label,
        1,
        0
    )

    layout.addWidget(
        latcal_input,
        1,
        1
    )


    # ============================================
    # Dorscal
    # ============================================

    dorscal_label = QLabel(
        "Dorscal (m/pix):"
    )

    dorscal_input = QDoubleSpinBox()
    dorscal_input.setDecimals(8)
    dorscal_input.setRange(0.0, 1.0)
    dorscal_input.setSingleStep(0.00000001)
    dorscal_input.setValue(0.00027257)


    layout.addWidget(
        dorscal_label,
        2,
        0
    )

    layout.addWidget(
        dorscal_input,
        2,
        1
    )


    # ============================================
    # Poly 1
    # ============================================

    poly1_label = QLabel(
        "Poly 1:"
    )

    poly1_input = QSpinBox()
    poly1_input.setRange(0, 20)
    poly1_input.setValue(4)


    layout.addWidget(
        poly1_label,
        3,
        0
    )

    layout.addWidget(
        poly1_input,
        3,
        1
    )


    # ============================================
    # Poly 2
    # ============================================

    poly2_label = QLabel(
        "Poly 2:"
    )
    poly2_input = QSpinBox()
    poly2_input.setRange(0, 20)
    poly2_input.setValue(3)

    layout.addWidget(
        poly2_label,
        4,
        0
    )

    layout.addWidget(
        poly2_input,
        4,
        1
    )


    # ============================================
    # Poly 3
    # ============================================
    poly3_label = QLabel(
        "Poly 3:"
    )

    poly3_input = QSpinBox()
    poly3_input.setRange(0, 20)
    poly3_input.setValue(2)


    layout.addWidget(
        poly3_label,
        5,
        0
    )

    layout.addWidget(
        poly3_input,
        5,
        1
    )


    # ============================================
    # Tail Diameter
    # ============================================

    td_label = QLabel(
        "Tail Diameter (m):"
    )

    td_input = QDoubleSpinBox()
    td_input.setDecimals(5)
    td_input.setRange(0.0, 1.0)
    td_input.setSingleStep(0.00001)
    td_input.setValue(0.00225)


    layout.addWidget(
        td_label,
        6,
        0
    )

    layout.addWidget(
        td_input,
        6,
        1
    )


    # ============================================
    # Register Parameters Button
    # ============================================

    parameter_button = QPushButton(
        "Register Parameters"
    )


    layout.addWidget(
        parameter_button,
        7,
        0,
        1,
        2,
        Qt.AlignmentFlag.AlignCenter
    )


    parameter_button.setObjectName("primary")

    # Tooltips
    for label, field, text in (
        (fps_label, fps_input, "Camera frame rate (frames per second)"),
        (latcal_label, latcal_input, "Lateral (side view) calibration, meters per pixel"),
        (dorscal_label, dorscal_input, "Dorsal (top view) calibration, meters per pixel"),
        (poly1_label, poly1_input, "Polynomial order 1, for detrending (not yet available)"),
        (poly2_label, poly2_input, "Polynomial order 2, for detrending (not yet available)"),
        (poly3_label, poly3_input, "Polynomial order 3, for detrending (not yet available)"),
        (td_label, td_input, "Mouse tail diameter in meters"),
    ):
        label.setToolTip(text)
        field.setToolTip(text)

    parameter_status = QLabel("Parameters not registered")
    parameter_status.setObjectName("parameter_status")
    layout.addWidget(parameter_status, 8, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)


    return {
        "section":
            section,

        "parameter_status":
            parameter_status,

        "fps_input":
            fps_input,

        "latcal_input":
            latcal_input,

        "dorscal_input":
            dorscal_input,

        "poly1_input":
            poly1_input,

        "poly2_input":
            poly2_input,

        "poly3_input":
            poly3_input,

        "td_input":
            td_input,

        "parameter_button":
            parameter_button
    }


# ================================================
# Dataset / Variable Section
# ================================================

def create_selection_section():


    section = QWidget()


    layout = QGridLayout(
        section
    )
    layout.setContentsMargins(0, 0, 0, 0)


    # Dataset

    dataset_label = QLabel(
        "Dataset:"
    )

    dataset_selector = QComboBox()


    # Variable

    variable_label = QLabel(
        "Variable:"
    )

    variable_selector = QComboBox()


    layout.addWidget(dataset_label, 0, 0)
    layout.addWidget(dataset_selector, 0, 1)
    layout.addWidget(variable_label, 0, 2)
    layout.addWidget(variable_selector, 0, 3)

    raw_view_button = QPushButton("Show Raw")
    raw_view_button.setCheckable(True)
    raw_view_button.setToolTip("View the imported data (read only)")
    layout.addWidget(raw_view_button, 0, 4)

    # let the dropdowns take the extra width
    layout.setColumnStretch(1, 2)
    layout.setColumnStretch(3, 1)


    return {
        "section":
            section,

        "dataset_selector":
            dataset_selector,

        "variable_selector":
            variable_selector,

        "raw_view_button":
            raw_view_button
    }


# ================================================
# Processing Section
# ================================================

def create_processing_section():
    section = QGroupBox("3. Data Cleaning")
    layout = QGridLayout(section)

    preparation_group = QGroupBox()
    preparation_group.setObjectName("panel")
    preparation_layout = QHBoxLayout(preparation_group)

    #=========================================
    #Filter & crop limits (blank = no limit)
    #==========================================

    t_min_input = QLineEdit()
    t_max_input = QLineEdit()
    v_min_input = QLineEdit()
    v_max_input = QLineEdit()

    t_min_input.setPlaceholderText("start")
    t_max_input.setPlaceholderText("end")
    v_min_input.setPlaceholderText("min")
    v_max_input.setPlaceholderText("max")

    layout.addWidget(QLabel("Time min (s):"), 0,0)
    layout.addWidget(t_min_input,0,1)
    layout.addWidget(QLabel("Time max (s):"),0,2)
    layout.addWidget(t_max_input, 0,3)

    layout.addWidget(QLabel("Value min (pix):"),1,0)
    layout.addWidget(v_min_input,1,1)
    layout.addWidget(QLabel("Value max (pix):"),1,2)
    layout.addWidget(v_max_input,1,3)

    #=====================================================
    #buttons
    #=====================================================

    filter_button =  QPushButton(
        "Apply Filter"
    )
    filter_button.setObjectName("primary")

    remove_points_button = QPushButton (
        "Remove Bad Points (click graph)"
    )

    remove_points_button.setCheckable(
        True
    )

    reset_button = QPushButton (
        "Reset Data"
    )
    fill_gap_button = QPushButton(
        "Fill Gaps"
    )
    convert_button = QPushButton(
        "Convert and Detrend"
    )
    smooth_button = QPushButton(
        "Standardize and Smooth"
    )
    button_layout = QHBoxLayout()
    button_layout.addWidget(filter_button)
    button_layout.addWidget(remove_points_button)
    button_layout.addWidget(reset_button)
    layout.addLayout(button_layout, 2, 0, 1, 4)

    # these steps are not implemented yet
    for button in (fill_gap_button, convert_button, smooth_button):
        button.setEnabled(False)
        button.setToolTip("Not yet available")
        preparation_layout.addWidget(button)

    return {
        "section":
        section,
        "preparation_group":
        preparation_group,
        "t_min_input":
        t_min_input,
        "t_max_input":
        t_max_input,
        "v_min_input":
        v_min_input,
        "v_max_input":
        v_max_input,
        "filter_button":
        filter_button,
        "remove_points_button":
        remove_points_button,
        "reset_button":
        reset_button,
        "fill_gap_button":
        fill_gap_button,
        "convert_button":
        convert_button,
        "smooth_button":
        smooth_button
    }

# ================================================
# Kinematics Section
# ================================================

def create_kinematics_section():


    section = QGroupBox()
    section.setObjectName("panel")


    layout = QHBoxLayout(
        section
    )


    calculate_button = QPushButton(
        "Run Kinematics Test"
    )


    results_label = QLabel(
        "Uses fixed test values, not your data."
    )



    layout.addWidget(
        calculate_button
    )


    layout.addWidget(
        results_label,
        stretch=1
    )


    return {
        "section":
            section,

        "calculate_button":
            calculate_button,

        "results_label":
            results_label
    }


# ================================================
# Export Section
# ================================================

def create_export_section():


    section = QGroupBox()
    section.setObjectName("panel")


    layout = QGridLayout(
        section
    )


    export_data_button = QPushButton(
        "Export Processed CSV"
    )


    export_results_button = QPushButton(
        "Export Kinematic Results"
    )


    layout.addWidget(
        export_data_button,
        0,
        0
    )

    layout.addWidget(
        export_results_button,
        0,
        1
    )


    for button in (export_data_button, export_results_button):
        button.setEnabled(False)
        button.setToolTip("Not yet available")


    return {
        "section":
            section,

        "export_data_button":
            export_data_button,

        "export_results_button":
            export_results_button
    }