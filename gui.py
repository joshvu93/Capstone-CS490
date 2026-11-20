"""MiceLab GUI for processing paired dorsal/lateral DLC tracking data."""

from pathlib import Path
import os
import numpy as np
import pandas as pd
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from data import load_csv_files
from plotting import RawDataGraph, NavigationToolbar2QT
import kinematics
import processing
from layout import (
    create_import_section,
    create_parameter_section,
    create_selection_section,
    create_processing_section,
    create_kinematics_section,
    create_export_section,
)


class MainWindow(QMainWindow):
    """Coordinate the UI and pass each view through the processing stages."""

    # Keep a separate snapshot per stage so users can inspect intermediate results.
    STAGES = ("raw", "filtered", "filled", "detrended", "smoothed")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MiceLab — Swimming Kinematics")
        self.resize(1180, 900)
        # Raw DLC tables are the source of truth; stage_data holds derived tables
        # keyed first by workflow stage, then by camera view.
        self.raw_by_view = {}
        self.stage_data = {stage: {} for stage in self.STAGES}
        # Manual exclusions are row positions paired with the DLC coordinate column.
        self.manual_outliers = {}
        self.manual_history = []
        self.current_view = None
        self.metrics = None
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        content = QWidget()
        self.workflow_layout = QVBoxLayout(content)
        scroll.setWidget(content)
        imp = create_import_section()
        self.workflow_layout.addWidget(imp["section"])
        self.dorsal_button, self.dorsal_status = (
            imp["dorsal_button"],
            imp["dorsal_status"],
        )
        self.lateral_button, self.lateral_status = (
            imp["lateral_button"],
            imp["lateral_status"],
        )
        params = create_parameter_section()
        self.workflow_layout.addWidget(params["section"])
        self.fps_input, self.latcal_input, self.dorscal_input = (
            params["fps_input"],
            params["latcal_input"],
            params["dorscal_input"],
        )
        self.poly1_input, self.poly2_input, self.poly3_input = (
            params["poly1_input"],
            params["poly2_input"],
            params["poly3_input"],
        )
        self.td_input = params["td_input"]
        self.parameter_button = params["parameter_button"]
        self.workflow_layout.addWidget(self.parameter_button)
        selection = create_selection_section()
        self.workflow_layout.addWidget(selection["section"])
        self.dataset_selector, self.stage_selector, self.variable_selector = (
            selection["dataset_selector"],
            selection["stage_selector"],
            selection["variable_selector"],
        )
        self.manual_edit_button = selection["manual_edit_button"]
        self.undo_manual_button = selection["undo_button"]
        self.clear_manual_button = selection["clear_button"]
        self.graph = RawDataGraph(self)
        self.workflow_layout.addWidget(NavigationToolbar2QT(self.graph, self))
        self.workflow_layout.addWidget(self.graph)
        proc = create_processing_section()
        self.workflow_layout.addWidget(proc["section"])
        self.filter_button, self.fill_gap_button = (
            proc["filter_button"],
            proc["fill_gap_button"],
        )
        self.convert_button, self.smooth_button = (
            proc["convert_button"],
            proc["smooth_button"],
        )
        kin = create_kinematics_section()
        self.workflow_layout.addWidget(kin["section"])
        self.calculate_button, self.results_label = (
            kin["calculate_button"],
            kin["results_label"],
        )
        exports = create_export_section()
        self.workflow_layout.addWidget(exports["section"])
        self.export_data_button, self.export_results_button = (
            exports["export_data_button"],
            exports["export_results_button"],
        )
        self.workflow_layout.addStretch()
        self.dorsal_button.clicked.connect(lambda: self.import_view_csv("dorsal"))
        self.lateral_button.clicked.connect(lambda: self.import_view_csv("lateral"))
        self.dataset_selector.currentIndexChanged.connect(self.dataset_changed)
        self.stage_selector.currentIndexChanged.connect(self.update_raw_graph)
        self.variable_selector.currentIndexChanged.connect(self.update_raw_graph)
        self.filter_button.clicked.connect(self.filter_data)
        self.fill_gap_button.clicked.connect(self.fill_gaps)
        self.convert_button.clicked.connect(self.convert_detrend)
        self.smooth_button.clicked.connect(self.standardize_smooth)
        self.calculate_button.clicked.connect(self.calculate_kinematics)
        self.export_data_button.clicked.connect(self.export_processed_data)
        self.export_results_button.clicked.connect(self.export_results)
        self.parameter_button.clicked.connect(self.apply_parameters)
        self.manual_edit_button.toggled.connect(self._manual_edit_toggled)
        self.undo_manual_button.clicked.connect(self.undo_manual_outlier)
        self.clear_manual_button.clicked.connect(self.clear_manual_outliers)
        self.graph.point_selected.connect(self.toggle_manual_outlier)

    def apply_parameters(self):
        self.stage_data = {stage: {} for stage in self.STAGES}
        self.metrics = None
        self.stage_selector.setCurrentIndex(0)
        self.update_raw_graph()
        self.statusBar().showMessage(
            "Parameters applied. Run the processing steps again to refresh results.",
            6000,
        )

    def _parameters(self):
        return {
            "fps": self.fps_input.value(),
            "lateral": self.latcal_input.value(),
            "dorsal": self.dorscal_input.value(),
            "order": self.poly1_input.value(),
            "likelihood": self.poly2_input.value(),
            "smooth": self.poly3_input.value(),
            "tail_diameter": self.td_input.value(),
        }

    def _error(self, title, error):
        QMessageBox.critical(self, title, str(error))

    def import_view_csv(self, view):
        path, _ = QFileDialog.getOpenFileName(
            self,
            f"Select {view.capitalize()} DeepLabCut CSV",
            str(Path.home()),
            "CSV files (*.csv)",
        )
        if not path:
            return
        try:
            frame = load_csv_files([path])[0]
            coordinates = [
                c
                for c in frame.columns
                if isinstance(c, tuple)
                and len(c) >= 3
                and str(c[2]).lower() in ("x", "y")
            ]
            if not coordinates:
                raise ValueError("No x/y tracking coordinates were found in this CSV.")
        except Exception as exc:
            self._error("Could not import CSV", exc)
            return
        self.raw_by_view[view] = frame
        self.manual_outliers[view] = set()
        self.manual_history = [
            entry for entry in self.manual_history if entry[0] != view
        ]
        self.metrics = None
        for stage in self.STAGES:
            self.stage_data[stage].pop(view, None)
        if view == "dorsal":
            self.dorsal_status.setText(os.path.basename(path))
        else:
            self.lateral_status.setText(os.path.basename(path))
        self.dataset_selector.blockSignals(True)
        self.dataset_selector.clear()
        for name in ("dorsal", "lateral"):
            if name in self.raw_by_view:
                self.dataset_selector.addItem(name.capitalize())
        self.dataset_selector.blockSignals(False)
        self.dataset_selector.setCurrentText(view.capitalize())
        self.dataset_changed()
        self.statusBar().showMessage(f"Imported {len(frame)} frames from {path}", 6000)

    def dataset_changed(self, *_):
        label = self.dataset_selector.currentText()
        self.current_view = label.lower() if label else None
        self.variable_selector.clear()
        if self.current_view not in self.raw_by_view:
            return
        frame = self.raw_by_view[self.current_view]
        names = []
        for col in frame.columns[1:]:
            if (
                isinstance(col, tuple)
                and len(col) >= 3
                and str(col[2]).lower() in ("x", "y")
            ):
                key = f"{col[1]}_{str(col[2]).lower()}"
                if key not in names:
                    names.append(key)
        self.variable_selector.addItems(names)
        self.stage_selector.setCurrentIndex(0)
        self.update_raw_graph()

    def _display_series(self):
        view, variable = self.current_view, self.variable_selector.currentText()
        if view not in self.raw_by_view or not variable:
            return None, None
        stage_index = self.stage_selector.currentIndex()
        stage = self.STAGES[stage_index]
        frame = self.stage_data[stage].get(view)
        if frame is None:
            if stage == "raw":
                frame = self.raw_by_view[view]
            else:
                self.graph.show_message(
                    f"Run the {self.stage_selector.currentText().lower()} step to display this stage."
                )
                return None, None
        x = pd.to_numeric(frame.iloc[:, 0], errors="coerce").to_numpy(dtype=float)
        if stage_index < 3:
            part, axis = variable.rsplit("_", 1)
            col = next(
                (
                    c
                    for c in frame.columns
                    if isinstance(c, tuple)
                    and len(c) >= 3
                    and c[1] == part
                    and str(c[2]).lower() == axis
                ),
                None,
            )
            if col is None:
                return x, np.full(x.size, np.nan)
            y = pd.to_numeric(frame[col], errors="coerce").to_numpy(dtype=float)
        else:
            suffix = "_detrended_m" if stage_index == 3 else "_smooth_m"
            col = f"{variable}{suffix}"
            y = (
                frame[col].to_numpy(dtype=float)
                if col in frame
                else np.full(x.size, np.nan)
            )
        return x, y

    def update_raw_graph(self, *_):
        if self.current_view not in self.raw_by_view:
            return
        x, y = self._display_series()
        stage = self.stage_selector.currentText()
        if x is None:
            return
        stage_index = self.stage_selector.currentIndex()
        can_edit = stage_index < 2 and bool(self.variable_selector.currentText())
        self.manual_edit_button.setEnabled(can_edit)
        self.graph.manual_edit_enabled = (
            can_edit and self.manual_edit_button.isChecked()
        )
        variable = self.variable_selector.currentText()
        marked_frames, marked_values = None, None
        rows = []
        if can_edit:
            raw = self.raw_by_view[self.current_view]
            column = self._column_for_variable(self.current_view, variable)
            if column is not None:
                rows = sorted(
                    row
                    for row, selected_column in self.manual_outliers.get(
                        self.current_view, set()
                    )
                    if selected_column == column
                )
                marked_frames = pd.to_numeric(
                    raw.iloc[rows, 0], errors="coerce"
                ).to_numpy(dtype=float)
                marked_values = pd.to_numeric(
                    raw[column].iloc[rows], errors="coerce"
                ).to_numpy(dtype=float)
        self.graph.plot_data(
            x,
            y,
            variable,
            self.dataset_selector.currentText() + " — " + stage,
            processed=stage != "Raw",
            row_indices=np.arange(x.size),
            marked_frames=marked_frames,
            marked_values=marked_values,
            marked_row_indices=np.asarray(rows, dtype=int) if can_edit else None,
        )

    def _column_for_variable(self, view, variable):
        """Map a visible bodypart_axis name back to its DLC MultiIndex column."""
        if view not in self.raw_by_view or not variable:
            return None
        part, axis = variable.rsplit("_", 1)
        return next(
            (
                column
                for column in self.raw_by_view[view].columns
                if isinstance(column, tuple)
                and len(column) >= 3
                and column[1] == part
                and str(column[2]).lower() == axis
            ),
            None,
        )

    def _manual_edit_toggled(self, enabled):
        self.manual_edit_button.setText(
            "Manual outlier editing: on" if enabled else "Manual outlier editing: off"
        )
        self.graph.manual_edit_enabled = (
            enabled and self.stage_selector.currentIndex() < 2
        )
        self.update_raw_graph()
        if enabled:
            self.statusBar().showMessage(
                "Click a sample on the graph to mark it as an outlier; click a red X to restore it.",
                7000,
            )

    def _refresh_after_manual_edit(self, view):
        """Rebuild the filtered view and invalidate every later processing stage."""
        for stage in ("filtered", "filled", "detrended", "smoothed"):
            self.stage_data[stage].pop(view, None)
        self.metrics = None
        filtered = processing.filter_data(
            self.raw_by_view[view], likelihood_threshold=self.poly2_input.value()
        )
        self.stage_data["filtered"][view] = processing.apply_manual_outliers(
            filtered, self.manual_outliers.get(view, set())
        )
        self.update_raw_graph()

    def toggle_manual_outlier(self, row):
        """Toggle the selected sample for the currently displayed coordinate."""
        view = self.current_view
        column = self._column_for_variable(view, self.variable_selector.currentText())
        if view not in self.raw_by_view or column is None:
            return
        point = (int(row), column)
        selected = self.manual_outliers.setdefault(view, set())
        existed = point in selected
        if existed:
            selected.remove(point)
        else:
            selected.add(point)
        self.manual_history.append((view, point, existed))
        self._refresh_after_manual_edit(view)
        action = "Restored" if existed else "Marked"
        frame_number = self.raw_by_view[view].iloc[row, 0]
        self.statusBar().showMessage(
            f"{action} {self.variable_selector.currentText()} at frame {frame_number}.",
            5000,
        )

    def undo_manual_outlier(self):
        if not self.manual_history:
            return
        view, point, existed = self.manual_history.pop()
        selected = self.manual_outliers.setdefault(view, set())
        if existed:
            selected.add(point)
        else:
            selected.discard(point)
        self._refresh_after_manual_edit(view)

    def clear_manual_outliers(self):
        view = self.current_view
        if view not in self.manual_outliers or not self.manual_outliers[view]:
            return
        self.manual_outliers[view].clear()
        self.manual_history = [
            entry for entry in self.manual_history if entry[0] != view
        ]
        self._refresh_after_manual_edit(view)
        self.statusBar().showMessage(
            "Cleared manual outlier marks for this view.", 5000
        )

    def _require_import(self):
        if not self.raw_by_view:
            QMessageBox.information(
                self,
                "Import data first",
                "Choose a dorsal or lateral DeepLabCut CSV first.",
            )
            return False
        return True

    def filter_data(self):
        if not self._require_import():
            return
        try:
            threshold = self.poly2_input.value()
            self.stage_data["filled"].clear()
            self.stage_data["detrended"].clear()
            self.stage_data["smoothed"].clear()
            self.metrics = None
            for view, frame in self.raw_by_view.items():
                filtered = processing.filter_data(frame, likelihood_threshold=threshold)
                self.stage_data["filtered"][view] = processing.apply_manual_outliers(
                    filtered, self.manual_outliers.get(view, set())
                )
            self.stage_selector.setCurrentIndex(1)
            self.update_raw_graph()
            self.statusBar().showMessage(
                f"Filtered low confidence detections at likelihood {threshold:.2f}",
                6000,
            )
        except Exception as exc:
            self._error("Filtering failed", exc)

    def fill_gaps(self):
        if not self._require_import():
            return
        if any(view not in self.stage_data["filtered"] for view in self.raw_by_view):
            self.filter_data()
            if any(
                view not in self.stage_data["filtered"] for view in self.raw_by_view
            ):
                return
        try:
            self.stage_data["detrended"].clear()
            self.stage_data["smoothed"].clear()
            self.metrics = None
            for view, frame in self.stage_data["filtered"].items():
                self.stage_data["filled"][view] = processing.fill_frame_gaps(frame)
            self.stage_selector.setCurrentIndex(2)
            self.update_raw_graph()
        except Exception as exc:
            self._error("Spline interpolation failed", exc)

    def convert_detrend(self):
        if not self._require_import():
            return
        if any(view not in self.stage_data["filled"] for view in self.raw_by_view):
            self.fill_gaps()
        if any(view not in self.stage_data["filled"] for view in self.raw_by_view):
            return
        try:
            p = self._parameters()
            self.stage_data["smoothed"].clear()
            self.metrics = None
            for view, frame in self.stage_data["filled"].items():
                calibration = p[view]
                self.stage_data["detrended"][view] = (
                    processing.convert_and_detrend_frame(
                        frame, calibration, p["fps"], p["order"]
                    )
                )
            self.stage_selector.setCurrentIndex(3)
            self.update_raw_graph()
        except Exception as exc:
            self._error("Conversion or detrending failed", exc)

    def standardize_smooth(self):
        if not self._require_import():
            return
        if any(view not in self.stage_data["detrended"] for view in self.raw_by_view):
            self.convert_detrend()
        if any(view not in self.stage_data["detrended"] for view in self.raw_by_view):
            return
        try:
            self.metrics = None
            for view, frame in self.stage_data["detrended"].items():
                self.stage_data["smoothed"][view] = processing.standardize_smooth_frame(
                    frame, self.poly3_input.value()
                )
            self.stage_selector.setCurrentIndex(4)
            self.update_raw_graph()
            self.graph.plot_overview(self.stage_data["smoothed"])
            self.statusBar().showMessage(
                "Standardized and smoothed data; overview is shown above.", 6000
            )
        except Exception as exc:
            self._error("Smoothing failed", exc)

    def calculate_kinematics(self):
        if not self._require_import():
            return
        if any(view not in self.stage_data["smoothed"] for view in self.raw_by_view):
            self.standardize_smooth()
        if any(view not in self.stage_data["smoothed"] for view in self.raw_by_view):
            return
        try:
            p = self._parameters()
            rows = []
            for view, frame in self.stage_data["smoothed"].items():
                metrics = kinematics.calculate_kinematic_results(
                    frame, p["fps"], p["tail_diameter"]
                )
                rows.append({"view": view.capitalize(), **metrics})
            self.metrics = pd.DataFrame(rows).set_index("view")
            self.results_label.setText(
                self.metrics.to_string(float_format=lambda value: f"{value:.5g}")
            )
            self.graph.plot_overview(self.stage_data["smoothed"])
        except Exception as exc:
            self._error("Kinematics calculation failed", exc)

    def _processed_export_frame(self, view):
        frame = self.stage_data["smoothed"].get(view)
        if frame is None:
            return None
        output = frame.copy()
        # Add angular velocity as a frame-aligned derived series for the hindlimb overview/export.
        required = [
            f"{part}_{axis}_smooth_m"
            for part, axis in (
                ("MTP", "x"),
                ("MTP", "y"),
                ("Ankle", "x"),
                ("Ankle", "y"),
            )
        ]
        if all(col in output for col in required):
            angle = kinematics.calculate_hindfoot_angle(
                *(output[col].to_numpy(dtype=float) for col in required)
            )
            output["hindfoot_angle_rad"] = angle
            output["hindfoot_angular_velocity_rad_s"] = np.r_[
                kinematics.calculate_hindfoot_angular_velocity(angle, output["time_s"]),
                np.nan,
            ]
        return output

    def export_processed_data(self):
        if not self._require_import():
            return
        if not self.stage_data["smoothed"]:
            self.standardize_smooth()
        if not self.stage_data["smoothed"]:
            return
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save processed tracking data",
            "miceLab_processed.csv",
            "CSV files (*.csv)",
        )
        if not path:
            return
        try:
            # Prefix columns before joining views so similarly named landmarks stay distinct.
            combined = []
            for view in ("dorsal", "lateral"):
                frame = self._processed_export_frame(view)
                if frame is not None:
                    frame = frame.add_prefix(f"{view}_")
                    combined.append(frame)
            pd.concat(combined, axis=1).to_csv(path, index=False)
            self.statusBar().showMessage(f"Saved processed data to {path}", 7000)
        except Exception as exc:
            self._error("Export failed", exc)

    def export_results(self):
        if self.metrics is None:
            self.calculate_kinematics()
        if self.metrics is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Save kinematics table", "miceLab_kinematics.csv", "CSV files (*.csv)"
        )
        if not path:
            return
        try:
            self.metrics.to_csv(path)
            image_path = str(Path(path).with_suffix(".png"))
            self.graph.figure.savefig(image_path, dpi=180, bbox_inches="tight")
            self.statusBar().showMessage(
                f"Saved results to {path} and overview to {image_path}", 7000
            )
        except Exception as exc:
            self._error("Export failed", exc)
