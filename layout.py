# Imports

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QSpinBox,
    QDoubleSpinBox,
)


# ================================================
# Import Data Section
# ================================================


    
def create_import_section():

    section = QGroupBox("1. Input Data")
    layout = QVBoxLayout(section)

    # Dorsal data
    dorsal_label = QLabel("Dorsal Data (Top View)")
    dorsal_button = QPushButton("Choose Dorsal CSV")
    dorsal_status = QLabel("No dorsal file selected")

    # Lateral data
    lateral_label = QLabel("Lateral Data (Side View)")
    lateral_button = QPushButton("Choose Lateral CSV")
    lateral_status = QLabel("No lateral file selected")

    # Add widgets to layout
    layout.addWidget(dorsal_label)
    layout.addWidget(dorsal_button)
    layout.addWidget(dorsal_status)

    layout.addSpacing(15)

    layout.addWidget(lateral_label)
    layout.addWidget(lateral_button)
    layout.addWidget(lateral_status)

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
        "2. Enter Calibration Parameters"
    )


    layout = QGridLayout(
        section
    )


    layout.setHorizontalSpacing(
        10
    )

    layout.setVerticalSpacing(
        10
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

    poly2_input = QLineEdit()



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

    poly3_input = QLineEdit()


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
        "TD:"
    )

    td_input = QLineEdit()

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


    return {
        "section":
            section,

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


    section = QGroupBox(
        "3. Select Dataset and Variable"
    )


    layout = QGridLayout(
        section
    )


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


    layout.addWidget(
        dataset_label,
        0,
        0
    )

    layout.addWidget(
        dataset_selector,
        0,
        1
    )


    layout.addWidget(
        variable_label,
        1,
        0
    )

    layout.addWidget(
        variable_selector,
        1,
        1
    )


    return {
        "section":
            section,

        "dataset_selector":
            dataset_selector,

        "variable_selector":
            variable_selector
    }


# ================================================
# Processing Section
# ================================================

def create_processing_section():


    section = QGroupBox(
        "4. Process Data"
    )


    layout = QGridLayout(
        section
    )


    filter_button = QPushButton(
        "Filter Data"
    )


    fill_gap_button = QPushButton(
        "Fill Gaps"
    )


    convert_button = QPushButton(
        "Convert & Detrend"
    )


    smooth_button = QPushButton(
        "Standardize & Smooth"
    )


    layout.addWidget(
        filter_button,
        0,
        0
    )

    layout.addWidget(
        fill_gap_button,
        0,
        1
    )

    layout.addWidget(
        convert_button,
        1,
        0
    )

    layout.addWidget(
        smooth_button,
        1,
        1
    )


    return {
        "section":
            section,

        "filter_button":
            filter_button,

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


    section = QGroupBox(
        "5. Calculate Kinematics"
    )


    layout = QVBoxLayout(
        section
    )


    calculate_button = QPushButton(
        "Calculate Kinematics"
    )


    results_label = QLabel(
        "No kinematic results calculated."
    )


    results_label.setWordWrap(
        True
    )


    layout.addWidget(
        calculate_button,
        alignment=Qt.AlignmentFlag.AlignCenter
    )


    layout.addWidget(
        results_label
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


    section = QGroupBox(
        "6. Export"
    )


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


    return {
        "section":
            section,

        "export_data_button":
            export_data_button,

        "export_results_button":
            export_results_button
    }