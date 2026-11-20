"""Matplotlib canvases used by the MiceLab desktop application."""

import numpy as np
from PySide6.QtCore import Signal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT


class RawDataGraph(FigureCanvasQTAgg):
    point_selected = Signal(int)

    def __init__(self, parent=None):
        self.figure = Figure(figsize=(9, 4.5), dpi=100)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.setMinimumHeight(320)
        self.manual_edit_enabled = False
        self._sample_x = np.array([])
        self._sample_y = np.array([])
        self._sample_rows = np.array([], dtype=int)
        self.mpl_connect("button_press_event", self._handle_click)
        self.show_message("Import a dorsal or lateral CSV to begin")

    def show_message(self, message):
        self.axes.clear()
        self.axes.text(
            0.5,
            0.5,
            message,
            ha="center",
            va="center",
            transform=self.axes.transAxes,
            wrap=True,
        )
        self.axes.set_axis_off()
        self.draw_idle()

    def plot_data(
        self,
        frames,
        values,
        variable,
        dataset,
        processed=False,
        row_indices=None,
        marked_frames=None,
        marked_values=None,
        marked_row_indices=None,
    ):
        x = np.asarray(frames, dtype=float)
        y = np.asarray(values, dtype=float)
        if x.shape != y.shape:
            self.show_message("Frame and coordinate lengths differ")
            return
        rows = (
            np.arange(x.size, dtype=int)
            if row_indices is None
            else np.asarray(row_indices, dtype=int)
        )
        if rows.shape != x.shape:
            self.show_message("Frame and sample-index lengths differ")
            return
        valid = np.isfinite(x) & np.isfinite(y)
        if not valid.any() and marked_frames is None:
            self.show_message("No valid numeric data available")
            return
        self.axes.clear()
        self.axes.set_axis_on()
        if valid.any():
            self.axes.plot(
                x[valid],
                y[valid],
                linewidth=1.1,
                label="Processed" if processed else "Raw",
            )
        self._sample_x = x[valid]
        self._sample_y = y[valid]
        self._sample_rows = rows[valid]

        marked_x = np.array([], dtype=float)
        marked_y = np.array([], dtype=float)
        marked_rows = np.array([], dtype=int)
        if marked_frames is not None and marked_values is not None:
            marked_x = np.asarray(marked_frames, dtype=float)
            marked_y = np.asarray(marked_values, dtype=float)
            if marked_row_indices is not None:
                marked_rows = np.asarray(marked_row_indices, dtype=int)
            elif row_indices is None:
                marked_rows = np.arange(marked_x.size, dtype=int)
            else:
                marked_rows = rows
            if marked_rows.shape != marked_x.shape:
                self.show_message("Marked points and row indices differ in length")
                return
            marked = np.isfinite(marked_x) & np.isfinite(marked_y)
            marked_x, marked_y, marked_rows = (
                marked_x[marked],
                marked_y[marked],
                marked_rows[marked],
            )
            if marked_x.size:
                self.axes.scatter(
                    marked_x,
                    marked_y,
                    marker="x",
                    s=64,
                    linewidths=1.8,
                    color="#d62728",
                    label="Manually marked outlier",
                    zorder=4,
                )
                # Marked samples remain clickable so they can be restored.
                self._sample_x = np.r_[self._sample_x, marked_x]
                self._sample_y = np.r_[self._sample_y, marked_y]
                self._sample_rows = np.r_[self._sample_rows, marked_rows]

        title = f"{dataset} — {variable}"
        if self.manual_edit_enabled:
            title += " — click a point to mark / restore"
        self.axes.set_title(title)
        self.axes.set_xlabel("Frame")
        self.axes.set_ylabel(variable.replace("_", " "))
        self.axes.grid(True, alpha=0.25)
        if valid.any() or marked_x.size:
            self.axes.legend(loc="best")
        self.figure.tight_layout()
        self.draw_idle()

    def _handle_click(self, event):
        """Select the nearest plotted sample when manual editing is enabled."""
        if (
            not self.manual_edit_enabled
            or event.inaxes is not self.axes
            or event.x is None
            or event.y is None
            or self._sample_x.size == 0
        ):
            return
        points = self.axes.transData.transform(
            np.column_stack((self._sample_x, self._sample_y))
        )
        distances = np.hypot(points[:, 0] - event.x, points[:, 1] - event.y)
        nearest = int(np.argmin(distances))
        if distances[nearest] <= 12:
            self.point_selected.emit(int(self._sample_rows[nearest]))

    def plot_overview(self, datasets):
        self.figure.clear()
        axes = self.figure.subplots(max(1, len(datasets)), 1, squeeze=False).ravel()
        if not datasets:
            self.show_message("Run the processing workflow to create an overview")
            return
        for ax, (view, frame) in zip(axes, datasets.items()):
            time = frame["time_s"].to_numpy(dtype=float)
            columns = [c for c in frame if c.endswith("_smooth_m")]
            selected = [
                c
                for c in columns
                if any(
                    part in c
                    for part in ("SnoutTip", "TailBase", "TailTip", "MTP", "Ankle")
                )
            ]
            for col in selected:
                ax.plot(
                    time, frame[col], linewidth=0.9, label=col.replace("_smooth_m", "")
                )
            ax.set_title(f"{view.capitalize()} view — processed overview")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Position (m, centered)")
            ax.grid(True, alpha=0.25)
            if selected:
                ax.legend(ncol=3, fontsize=8)
        self.figure.tight_layout()
        self.draw_idle()
