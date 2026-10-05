# Imports

import os

from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from layout import (
    create_import_section,
    create_parameter_section,
    create_selection_section,
    create_processing_section,
    create_kinematics_section,
    create_export_section,
)

from data import (
    load_csv_files,
    extract_variables,
)

import kinematics


# GUI

class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()


        # ============================================
        # Window settings
        # ============================================

        self.setWindowTitle(
            "MiceLab"
        )

        self.resize(
            1100,
            800
        )


        # ============================================
        # Data storage
        # ============================================

        self.file_paths = []

        self.data = []

        self.standardized_data = []


        # ============================================
        # Main container
        # ============================================

        main_container = QWidget()

        self.setCentralWidget(
            main_container
        )


        main_layout = QVBoxLayout(
            main_container
        )


        # ============================================
        # Scroll area
        # ============================================

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )


        # Container inside scroll area

        workflow_container = QWidget()

        self.workflow_layout = QVBoxLayout(
            workflow_container
        )

        self.workflow_layout.setSpacing(
            15
        )


        # ============================================
        # Import Data
        # ============================================

        import_section = (
            create_import_section()
        )

        self.workflow_layout.addWidget(
            import_section["section"]
        )

        self.import_button = (
            import_section[
                "import_button"
            ]
        )

        self.file_status = (
            import_section[
                "file_status"
            ]
        )


        # ============================================
        # Parameters
        # ============================================

        parameter_section = (
            create_parameter_section()
        )

        self.workflow_layout.addWidget(
            parameter_section[
                "section"
            ]
        )


        self.fps_input = (
            parameter_section[
                "fps_input"
            ]
        )

        self.latcal_input = (
            parameter_section[
                "latcal_input"
            ]
        )

        self.dorscal_input = (
            parameter_section[
                "dorscal_input"
            ]
        )

        self.poly1_input = (
            parameter_section[
                "poly1_input"
            ]
        )

        self.poly2_input = (
            parameter_section[
                "poly2_input"
            ]
        )

        self.poly3_input = (
            parameter_section[
                "poly3_input"
            ]
        )

        self.td_input = (
            parameter_section[
                "td_input"
            ]
        )

        self.parameter_button = (
            parameter_section[
                "parameter_button"
            ]
        )


        # ============================================
        # Dataset / Variable Selection
        # ============================================

        selection_section = (
            create_selection_section()
        )

        self.workflow_layout.addWidget(
            selection_section[
                "section"
            ]
        )


        self.dataset_selector = (
            selection_section[
                "dataset_selector"
            ]
        )

        self.variable_selector = (
            selection_section[
                "variable_selector"
            ]
        )


        # ============================================
        # Processing
        # ============================================

        processing_section = (
            create_processing_section()
        )

        self.workflow_layout.addWidget(
            processing_section[
                "section"
            ]
        )


        self.filter_button = (
            processing_section[
                "filter_button"
            ]
        )

        self.fill_gap_button = (
            processing_section[
                "fill_gap_button"
            ]
        )

        self.convert_button = (
            processing_section[
                "convert_button"
            ]
        )

        self.smooth_button = (
            processing_section[
                "smooth_button"
            ]
        )


        # ============================================
        # Kinematics
        # ============================================

        kinematics_section = (
            create_kinematics_section()
        )

        self.workflow_layout.addWidget(
            kinematics_section[
                "section"
            ]
        )


        self.calculate_button = (
            kinematics_section[
                "calculate_button"
            ]
        )

        self.results_label = (
            kinematics_section[
                "results_label"
            ]
        )


        # ============================================
        # Export
        # ============================================

        export_section = (
            create_export_section()
        )

        self.workflow_layout.addWidget(
            export_section[
                "section"
            ]
        )


        self.export_data_button = (
            export_section[
                "export_data_button"
            ]
        )

        self.export_results_button = (
            export_section[
                "export_results_button"
            ]
        )


        # Push sections toward top

        self.workflow_layout.addStretch()


        # Put workflow into scroll area

        self.scroll_area.setWidget(
            workflow_container
        )


        # Add scroll area to window

        main_layout.addWidget(
            self.scroll_area
        )


        # ============================================
        # Connect buttons
        # ============================================

        self.import_button.clicked.connect(
            self.import_csv
        )

        self.parameter_button.clicked.connect(
            self.register_parameters
        )

        self.calculate_button.clicked.connect(
            self.calculate_kinematics
        )


        # Dataset selector

        self.dataset_selector.currentIndexChanged.connect(
            self.dataset_changed
        )


        # Processing buttons

        self.filter_button.clicked.connect(
            self.filter_data
        )

        self.fill_gap_button.clicked.connect(
            self.fill_gaps
        )

        self.convert_button.clicked.connect(
            self.convert_detrend
        )

        self.smooth_button.clicked.connect(
            self.standardize_smooth
        )


        # Export buttons

        self.export_data_button.clicked.connect(
            self.export_processed_data
        )

        self.export_results_button.clicked.connect(
            self.export_results
        )


    # ============================================
    # Register parameters
    # ============================================

    def register_parameters(self):


        self.fps = (
            self.fps_input.text()
        )

        self.latcal = (
            self.latcal_input.text()
        )

        self.dorscal = (
            self.dorscal_input.text()
        )

        self.poly1 = (
            self.poly1_input.text()
        )

        self.poly2 = (
            self.poly2_input.text()
        )

        self.poly3 = (
            self.poly3_input.text()
        )

        self.td = (
            self.td_input.text()
        )


        # Console confirmation

        print(
            "Parameters registered:"
        )

        print(
            f"FPS: {self.fps}"
        )

        print(
            f"Latcal: {self.latcal}"
        )

        print(
            f"Dorscal: {self.dorscal}"
        )

        print(
            f"Poly 1: {self.poly1}"
        )

        print(
            f"Poly 2: {self.poly2}"
        )

        print(
            f"Poly 3: {self.poly3}"
        )

        print(
            f"TD: {self.td}"
        )


    # ============================================
    # Import CSV
    # ============================================

    def import_csv(self):


        # Open file picker

        file_paths, _ = (
            QFileDialog.getOpenFileNames(
                self,
                "Select CSV Files",
                "",
                "CSV Files (*.csv)"
            )
        )


        # Stop if nothing selected

        if not file_paths:

            return


        # Store paths

        self.file_paths = (
            file_paths
        )


        # Load datasets

        self.data = load_csv_files(
            self.file_paths
        )


        # Store standardized variables
        # for each dataset

        self.standardized_data = []


        for dataset in self.data:

            variables = (
                extract_variables(
                    dataset
                )
            )

            self.standardized_data.append(
                variables
            )


        # ============================================
        # Update dataset selector
        # ============================================

        self.dataset_selector.clear()


        for file_path in self.file_paths:

            file_name = os.path.basename(
                file_path
            )

            self.dataset_selector.addItem(
                file_name
            )


        # Update status

        self.file_status.setText(
            f"{len(self.data)} CSV file(s) loaded."
        )


        print(
            f"Loaded {len(self.data)} CSV file(s)."
        )


        # Load variable selector

        if self.data:

            self.dataset_changed(
                0
            )


    # ============================================
    # Dataset changed
    # ============================================

    def dataset_changed(
        self,
        index
    ):


        if (
            index < 0
            or
            index >= len(
                self.standardized_data
            )
        ):

            return


        variables = (
            self.standardized_data[
                index
            ]
        )


        # Clear variable selector

        self.variable_selector.clear()


        # Only display variables that exist

        for variable_name, values in variables.items():

            if values is not None:

                self.variable_selector.addItem(
                    variable_name
                )


    # ============================================
    # Processing placeholders
    # ============================================

    def filter_data(self):

        print(
            "Filter Data clicked."
        )

        print(
            "Filtering will be implemented in processing.py."
        )


    def fill_gaps(self):

        print(
            "Fill Gaps clicked."
        )

        print(
            "Gap filling will be implemented in processing.py."
        )


    def convert_detrend(self):

        print(
            "Convert / Detrend clicked."
        )

        print(
            "Conversion and detrending will be implemented in processing.py."
        )


    def standardize_smooth(self):

        print(
            "Standardize / Smooth clicked."
        )

        print(
            "Standardization and smoothing will be implemented in processing.py."
        )


    # ============================================
    # Calculate Kinematics
    # ============================================

    def calculate_kinematics(self):


        print(
            "\nKINEMATIC RESULTS"
        )

        print(
            "------------------"
        )


        # Test time calculation

        test_time = (
            kinematics.calculate_time(
                250,
                250
            )
        )

        print(
            f"Time test: {test_time}"
        )


        # Test virtual mass calculation

        test_mass = (
            kinematics.calculate_virtual_mass(
                0.00225
            )
        )

        print(
            f"Virtual mass test: {test_mass}"
        )


        # Show temporary results in GUI

        self.results_label.setText(
            "Kinematic functions connected.\n"
            f"Time test: {test_time}\n"
            f"Virtual mass test: {test_mass}"
        )


        # ========================================
        # Future kinematic pipeline
        # ========================================

        # fps = float(self.fps)
        # latcal = float(self.latcal)
        # dorscal = float(self.dorscal)
        # td = float(self.td)
        #
        #
        # variables = self.standardized_data[
        #     self.dataset_selector.currentIndex()
        # ]
        #
        #
        # time = kinematics.calculate_time(
        #     variables["frame"],
        #     fps
        # )
        #
        #
        # TODO:
        #
        # processed_snout_x
        # processed_tail_tip_x
        # processed_tail_tip_y
        # processed_tail_base_y
        # processed_mtp_x
        # processed_mtp_y
        # processed_ankle_x
        # processed_ankle_y
        #
        # will come from processing.py later.


    # ============================================
    # Export placeholders
    # ============================================

    def export_processed_data(self):

        print(
            "Export Processed Data clicked."
        )


    def export_results(self):

        print(
            "Export Results clicked."
        )