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
)


# ================================================
# Import Data Section
# ================================================

def create_import_section():


    section = QGroupBox(
        "1. Import Data"
    )


    layout = QVBoxLayout(
        section
    )


    # Import button

    import_button = QPushButton(
        "Import CSV Files"
    )


    # Status

    file_status = QLabel(
        "No CSV files loaded."
    )


    layout.addWidget(
        import_button,
        alignment=Qt.AlignmentFlag.AlignCenter
    )


    layout.addWidget(
        file_status,
        alignment=Qt.AlignmentFlag.AlignCenter
    )


    return {
        "section": section,

        "import_button":
            import_button,

        "file_status":
            file_status
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

    fps_input = QLineEdit()

    fps_input.setPlaceholderText(
        "Enter FPS value"
    )


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

    latcal_input = QLineEdit()

    latcal_input.setPlaceholderText(
        "Enter Latcal value"
    )


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

    dorscal_input = QLineEdit()

    dorscal_input.setPlaceholderText(
        "Enter Dorscal value"
    )


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

    poly1_input = QLineEdit()

    poly1_input.setPlaceholderText(
        "Enter Poly 1 value"
    )


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

    poly2_input = QLineEdit()

    poly2_input.setPlaceholderText(
        "Enter Poly 2 value"
    )


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

    poly3_input = QLineEdit()

    poly3_input.setPlaceholderText(
        "Enter Poly 3 value"
    )


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

    td_input.setPlaceholderText(
        "Enter TD value"
    )


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