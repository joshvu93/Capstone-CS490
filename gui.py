# Imports

import os
import copy
import numpy as np 
import processing 
from plotting import RawDataGraph, NavigationToolbar2QT
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QFileDialog,
    QPushButton,
    QLabel,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from data import (
    load_csv_files,
    extract_variables,
)
import kinematics

from layout import (
    create_import_section,
    create_parameter_section,
    create_selection_section,
    create_processing_section,
    create_kinematics_section,
    create_export_section,
)

# turns "tail_tip_y" into "Tail Tip Y" for display
def readable_name(variable):
    return variable.replace("_", " ").title().replace("Mtp", "MTP")


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
            1280,
            780
        )

        # smaller than this and the panels start to overlap the graph
        self.setMinimumSize(1080, 680)


        # styles.qss is a light theme, so don't follow macOS dark mode
        # (setColorScheme needs Qt 6.8 or newer)
        hints = QGuiApplication.styleHints()
        if hasattr(hints, "setColorScheme"):
            hints.setColorScheme(Qt.ColorScheme.Light)


        # ============================================
        # Data storage
        # ============================================

        self.file_paths = []

        self.data = []

        self.standardized_data = []

        self.original_data = []

        # ============================================
        # Main container
        # ============================================

        main_container = QWidget()

        self.setCentralWidget(
            main_container
        )


        main_layout = QHBoxLayout(
            main_container
        )

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        main_layout.addWidget(splitter)


        # ============================================
        # Left sidebar
        # ============================================

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setMinimumWidth(290)

        # Use smaller steps for mouse-wheel scrolling
        self.scroll_area.verticalScrollBar().setSingleStep(12)

        sidebar_container = QWidget()
        self.sidebar_layout = QVBoxLayout(sidebar_container)
        self.sidebar_layout.setContentsMargins(0, 0, 4, 0)
        self.scroll_area.setWidget(sidebar_container)


        # ============================================
        # Right workspace
        # ============================================

        workspace_container = QWidget()
        self.workflow_layout = QVBoxLayout(workspace_container)
        self.workflow_layout.setContentsMargins(4, 0, 0, 0)

        splitter.addWidget(self.scroll_area)
        splitter.addWidget(workspace_container)

        # extra width goes to the workspace
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([300, 980])


        # ============================================
        # Import Data
        # ============================================

        import_section = (
            create_import_section()
        )

        self.sidebar_layout.addWidget(
            import_section["section"]
        )

        self.dorsal_button = import_section["dorsal_button"]
        self.dorsal_status = import_section["dorsal_status"]

        self.lateral_button = import_section["lateral_button"]
        self.lateral_status = import_section["lateral_status"]
        

        # ============================================
        # Parameters
        # ============================================

        parameter_section = (
            create_parameter_section()
        )

        self.sidebar_layout.addWidget(
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


        # keep sidebar sections at the top
        self.sidebar_layout.addStretch()


        self.parameter_status = parameter_section["parameter_status"]


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

        self.raw_view_button = selection_section["raw_view_button"]

        # ============================================
        # Raw Data Graph
        # ============================================

        self.raw_graph = RawDataGraph(self)

        self.graph_toolbar = NavigationToolbar2QT(
            self.raw_graph,
            self
        )

        self.graph_toolbar.setIconSize(QSize(18, 18))

        self.workflow_layout.addWidget(
            self.graph_toolbar
        )

        self.remove_hint = QLabel(
            "Click a point on the graph to remove it. "
            "Turn off zoom/pan first."
        )
        self.remove_hint.hide()
        self.workflow_layout.addWidget(self.remove_hint)

        self.workflow_layout.addWidget(
            self.raw_graph,
            stretch=1
        )

        self.variable_selector.currentIndexChanged.connect(
            self.update_raw_graph
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

        self.t_min_input = processing_section["t_min_input"]
        self.t_max_input = processing_section["t_max_input"]
        self.v_min_input = processing_section["v_min_input"]
        self.v_max_input = processing_section["v_max_input"]

        self.remove_points_button = processing_section["remove_points_button"]
        self.reset_button = processing_section["reset_button"]

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


        # ============================================
        # Collapsible panels (one open at a time)
        # ============================================

        toggle_layout = QHBoxLayout()
        self.workflow_layout.insertLayout(
            self.workflow_layout.indexOf(processing_section["section"]) + 1,
            toggle_layout
        )
        self.workflow_layout.insertWidget(
            self.workflow_layout.indexOf(kinematics_section["section"]),
            processing_section["preparation_group"]
        )

        self.panels = []

        for title, panel in (
            ("4. Preparation (not ready)", processing_section["preparation_group"]),
            ("5. Kinematics (test only)", kinematics_section["section"]),
            ("6. Export (not ready)", export_section["section"]),
        ):
            button = QPushButton("\u25b8 " + title)
            button.setCheckable(True)
            toggle_layout.addWidget(button)
            panel.hide()
            self.panels.append((button, panel))
            button.clicked.connect(
                lambda checked, opened=button: self.toggle_panel(opened)
            )


        # ============================================
        # Status bar
        # ============================================

        self.status_summary = QLabel()
        self.statusBar().addPermanentWidget(self.status_summary)


        # ============================================
        # Connect buttons
        # ============================================

       
        self.dorsal_button.clicked.connect(
            lambda: self.import_view_csv("dorsal")
        )

        self.lateral_button.clicked.connect(
            lambda: self.import_view_csv("lateral")
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

        self.reset_button.clicked.connect(
            self.reset_data
        )

        self.raw_graph.mpl_connect(
            "button_press_event",
            self.graph_clicked
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


        self.raw_view_button.toggled.connect(
            lambda: self.update_raw_graph()
        )

        self.remove_points_button.toggled.connect(
            self.remove_hint.setVisible
        )

        # any parameter edit means it has to be registered again
        for field in (
            self.fps_input, self.latcal_input, self.dorscal_input,
            self.poly1_input, self.poly2_input, self.poly3_input,
            self.td_input,
        ):
            field.valueChanged.connect(self.parameters_changed)


        # Export buttons

        self.export_data_button.clicked.connect(
            self.export_processed_data
        )

        self.export_results_button.clicked.connect(
            self.export_results
        )

        self.update_buttons()
        self.update_status()


    # ============================================
    # Register parameters
    # ============================================

    def register_parameters(self):


        self.fps = (
            self.fps_input.value()
        )

        self.latcal = (
            self.latcal_input.value()
        )

        self.dorscal = (
            self.dorscal_input.value()
        )

        self.poly1 = (
            self.poly1_input.value()
        )

        self.poly2 = (
            self.poly2_input.value()
        )

        self.poly3 = (
            self.poly3_input.value()
        )

        self.td = (
            self.td_input.value()
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
            f"Tail Diameter (m): {self.td}"
        )


        self.parameter_status.setText("\u2713 Parameters registered")
        self.set_success(self.parameter_status, True)
        self.update_status()


    def parameters_changed(self):
        self.parameter_status.setText("Parameters not registered")
        self.set_success(self.parameter_status, False)
        self.update_status()


    def set_success(self, label, success):
        label.setProperty("success", success)

        # re-apply styles.qss after changing the property
        label.style().unpolish(label)
        label.style().polish(label)


    def toggle_panel(self, opened):
        for button, panel in self.panels:
            if button is not opened:
                button.setChecked(False)
            panel.setVisible(button.isChecked())
            arrow = "\u25be" if button.isChecked() else "\u25b8"
            button.setText(arrow + button.text()[1:])


    def update_status(self):
        # processed if any array differs from the import
        processed = any(
            not np.array_equal(original[name], values, equal_nan=True)
            for original, current in zip(self.original_data, self.standardized_data)
            for name, values in current.items()
        )

        if not self.standardized_data:
            state = "no data"
        elif processed:
            state = "processed"
        else:
            state = "raw"

        registered = self.parameter_status.text().startswith("\u2713")

        self.status_summary.setText(
            f"Datasets: {len(self.standardized_data)}  |  "
            f"Calibration: {'registered' if registered else 'not registered'}  |  "
            f"Data: {state}"
        )


    # ============================================
    # Enable / disable actions
    # ============================================

    def update_buttons(self):
        has_data = bool(self.standardized_data)
        variable = self.variable_selector.currentData()
        # raw view is read only
        can_edit = (
            has_data
            and variable not in (None, "frame")
            and not self.raw_view_button.isChecked()
        )

        self.dataset_selector.setEnabled(has_data)
        self.variable_selector.setEnabled(has_data)
        self.filter_button.setEnabled(can_edit)
        self.remove_points_button.setEnabled(can_edit)
        self.reset_button.setEnabled(has_data)
        self.raw_view_button.setEnabled(has_data)

        for field in (
            self.t_min_input, self.t_max_input,
            self.v_min_input, self.v_max_input,
        ):
            field.setEnabled(can_edit)

        if not can_edit:
            self.remove_points_button.setChecked(False)


    # ============================================
    # Import CSV
    # ============================================

   
    def import_view_csv(self, view):

        # Open file picker for dorsal or lateral data
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select {view.capitalize()} CSV",
            "",
            "CSV Files (*.csv)"
        )

        # Stop if user cancels
        if not file_path:
            return

        # Remember each selected file
        if not hasattr(self, "view_files"):
            self.view_files = {}

        self.view_files[view] = file_path

        # Update the correct filename label and button
        if view == "dorsal":
            status, button = self.dorsal_status, self.dorsal_button
        else:
            status, button = self.lateral_status, self.lateral_button

        status.setText(
            "\u2713 " + status.fontMetrics().elidedText(
                os.path.basename(file_path),
                Qt.TextElideMode.ElideMiddle,
                210
            )
        )
        status.setToolTip(file_path)
        self.set_success(status, True)
        button.setText(f"Replace {view.capitalize()} CSV")

        # Load available datasets in a fixed order
        self.file_paths = [
            self.view_files[key]
            for key in ("dorsal", "lateral")
            if key in self.view_files
        ]

        # Read CSV files
        self.data = load_csv_files(self.file_paths)

        # Extract tracking variables
        self.standardized_data = [
            extract_variables(dataset)
            for dataset in self.data
        ]
        self.original_data = copy.deepcopy(
            self.standardized_data
        )
        # Update dataset dropdown
        self.raw_view_button.setChecked(False)
        self.dataset_selector.blockSignals(True)
        self.dataset_selector.clear()

        for path in self.file_paths:
            self.dataset_selector.addItem(
                os.path.basename(path)
            )

        self.dataset_selector.blockSignals(False)

        # Refresh variable selector and graph
        if self.data:
            self.dataset_selector.setCurrentIndex(0)
            self.dataset_changed(0)

        print(
            f"Loaded {len(self.data)} CSV file(s)."
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
                    readable_name(variable_name),
                    variable_name
                )
        self.update_raw_graph()
    # ============================================
    # Update Raw Data Graph
    # ============================================

    def update_raw_graph(self, index=None,keep_view=False):

        dataset_index = self.dataset_selector.currentIndex()
        variable = self.variable_selector.currentData()

        self.update_buttons()
        self.update_status()

        if not (0 <= dataset_index < len(self.standardized_data)):
            return

        variables = self.standardized_data[dataset_index]

        show_raw = self.raw_view_button.isChecked()

        if show_raw:
            variables = self.original_data[dataset_index]

        if not variable or variable == "frame":
            self.raw_graph.show_message(
                "Select a tracking coordinate"
            )
            return

        frames = variables.get("frame")
        values = variables.get(variable)

        if frames is None or values is None:
            self.raw_graph.show_message(
                "This variable is unavailable"
            )
            return

        dataset_name = self.dataset_selector.currentText()

        #time axis so filter limits match R work flow 

        time = np.asarray(frames, dtype=float)/self.fps_input.value()

        #work out which points were removed compared with the import 

        removed_x = removed_y = None 

        if not show_raw and dataset_index < len(self.original_data):
            original = self.original_data[dataset_index]
            if original.get(variable) is not None:
                keep = np.isin(
                    np.asarray(original["frame"]),
                    np.asarray(frames)
                )
                orig_values = np.asarray(
                    original[variable],
                    dtype=float
                )[keep]
                if orig_values.shape == time.shape:
                    removed = (
                        np.isfinite(orig_values)
                        & ~np.isfinite(np.asarray(values,dtype=float))
                    )
                    removed_x = time[removed]
                    removed_y = orig_values[removed]
        if show_raw:
            state = "Raw data, as imported"
        elif np.array_equal(
            self.original_data[dataset_index][variable], values, equal_nan=True
        ):
            state = "Raw data, no changes yet"
        else:
            state = "Processed data"

        path = self.file_paths[dataset_index]
        view = "Dorsal" if path == self.view_files.get("dorsal") else "Lateral"

        name = readable_name(variable)

        self.raw_graph.plot_data(
            time, values, name, dataset_name, x_label="Time (s)", keep_view=keep_view, removed_x =removed_x, removed_y =removed_y,
            title=name,
            subtitle=f"{view} view  |  {state}"
        )


    # ============================================
    # Processing placeholders
    # ============================================

    def filter_data(self):
        print ("Filter data clicked.")

        try: 
            self._filter_data_impl()
        except Exception as error: 
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Filter error",
                f"{type(error).__name__}:{error}"
            )
    def _filter_data_impl(self):

        index, variable = self._current_selection()

        if index is None:
            return

        ok1, t_min = self._read_limit(self.t_min_input, "Time min")
        ok2, t_max = self._read_limit(self.t_max_input, "Time max")
        ok3, v_min = self._read_limit(self.v_min_input, "Value min")
        ok4, v_max = self._read_limit(self.v_max_input, "Value max")

        if not (ok1 and ok2 and ok3 and ok4):
            return

        if (
            t_min is not None and t_max is not None and t_min >= t_max
        ) or (
            v_min is not None and v_max is not None and v_min >= v_max
        ):
            QMessageBox.warning(
                self,
                "Invalid range",
                "Min must be smaller than max."
            )
            return

        variables = self.standardized_data[index]

        # No limits entered -> automatic glitch removal in one click
        if (
            t_min is None and t_max is None
            and v_min is None and v_max is None
        ):

            values = np.asarray(variables[variable], dtype=float)

            before = int(np.isfinite(values).sum())

            variables[variable] = processing.remove_spikes(values)

            after = int(np.isfinite(variables[variable]).sum())

            message = (
                f"Filter applied to {readable_name(variable)}: "
                f"{before - after} point(s) removed."
            )

            print(message)
            self.statusBar().showMessage(message, 8000)

            self.update_raw_graph()

            return

        fps = self.fps_input.value()

        before = int(np.isfinite(np.asarray(variables[variable], dtype=float)).sum())

        # 1. Crop every variable to the time window
        cropped = processing.crop_variables(
            variables,
            fps,
            t_min,
            t_max
        )

        if len(cropped["frame"]) == 0:

            QMessageBox.warning(
                self,
                "Nothing left",
                "No frames fall inside that time window."
            )

            return

        in_window = int(np.isfinite(np.asarray(cropped[variable], dtype=float)).sum())

        # 2. Out-of-range values in the selected variable -> NaN
        cropped[variable] = processing.threshold_values(
            cropped[variable],
            v_min,
            v_max
        )

        self.standardized_data[index] = cropped

        kept = int(np.isfinite(cropped[variable]).sum())

        message = (
            f"Filter applied to {readable_name(variable)}: "
            f"{before - kept} point(s) removed "
            f"({before - in_window} by time, {in_window - kept} by value)."
        )

        print(message)
        self.statusBar().showMessage(message, 8000)

        self.update_raw_graph()
          

    def _read_limit (self, line_edit, label):
        text =line_edit.text().strip()

        if not text:
            return True, None
        try: 
            return True, float(text)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid value",
                f"{label} must be a number"
            )
            return False, None
    def _current_selection(self):

        #return data, index, variable or none
        index = self.dataset_selector.currentIndex()
        variable = self.variable_selector.currentData()

        if not (0 <= index <len(self.standardized_data)):
            QMessageBox.information(
                self,
                "No data",
                "Import a CSV file first."
            )

            return None, None
        if not variable or variable == "frame":

            QMessageBox.information(
                self,
                "Select a variable",
                "Select a tracking coordinate to filter."
            )

            return None, None

        return index, variable
    
    def graph_clicked(self, event):
        # only active when "Remove Bad Points" is toggled on
        if not self.remove_points_button.isChecked():
            return

        # ignore clicks used by the zoom/pan tool
        if self.graph_toolbar.mode != "":
            return

        if event.inaxes is not self.raw_graph.axes or event.button != 1:
            return

        index, variable = self._current_selection()
        if index is None:
            return

        point = self.raw_graph.nearest_point(event)
        if point is None:
            return

        variables = self.standardized_data[index]

        variables[variable] = processing.remove_bad_point(
            variables[variable],
            point
        )

        print(f"Removed {variable} point at index {point}.")
        self.update_raw_graph(keep_view=True)
    def reset_data (self):
        if not self.original_data:
            return
        self.standardized_data = copy.deepcopy(
            self.original_data
        )
        self.update_raw_graph()
        print(
            "Data Reset to original import"
        )
        self.statusBar().showMessage("Data reset to original import.", 8000)
    def fill_gaps(self):
        print ("button pressed")
    def convert_detrend(self):
        print ("button pressed")
    def standardize_smooth(self):
        print ("button pressed")



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
            f"Time test: {test_time:.2f} s\n"
            f"Virtual mass test: {test_mass:.4g}"
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