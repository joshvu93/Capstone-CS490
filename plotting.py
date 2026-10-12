
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT


class RawDataGraph(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.setMinimumHeight(350)
        self.show_message("Import CSV files to display data")

    def show_message(self, message):
        self.axes.clear()
        self.axes.text(
            0.5, 0.5, message,
            ha="center", va="center",
            transform=self.axes.transAxes
        )
        self.axes.set_axis_off()
        self.draw_idle()

    def plot_data(self, frames, values, variable, dataset):
        x = np.asarray(frames, dtype=float)
        y = np.asarray(values, dtype=float)

        if x.shape != y.shape:
            self.show_message("Frame and coordinate lengths differ")
            return

        valid = np.isfinite(x) & np.isfinite(y)

        if not valid.any():
            self.show_message("No valid numeric data available")
            return

        self.axes.clear()
        self.axes.set_axis_on()
        self.axes.plot(x, y, linewidth=1.2)

        self.axes.set_title(f"{dataset} — {variable}")
        self.axes.set_xlabel("Frame")
        self.axes.set_ylabel(f"{variable} (pixels)")
        self.axes.grid(True, alpha=0.25)

        self.figure.tight_layout()
        self.draw_idle()
