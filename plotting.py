
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT


class RawDataGraph(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(10, 5), dpi=100, layout="tight")
        self.axes = self.figure.add_subplot(111)
        super().__init__(self.figure)
        self.setParent(parent)
        self.setMinimumHeight(200)
        self.show_message("Import CSV files to display data")

    def show_message(self, message):
        self.current_x = None 
        self.current_y = None 
        self.axes.clear()
        self.axes.text(
            0.5, 0.5, message,
            ha="center", va="center",
            transform=self.axes.transAxes
        )
        self.axes.set_axis_off()
        self.draw_idle()


    def plot_data(
            self, 
            x_values,
            values, 
            variable, 
            dataset,
            x_label="Frame",
            keep_view =False,
            removed_x=None, 
            removed_y=None,
            title=None,
            subtitle=None
            ):
        x = np.asarray(x_values, dtype=float)
        y = np.asarray(values, dtype=float)
        if x.shape != y.shape:
            self.show_message("X and coordinate lengths differ")
            return 
        
        valid = np.isfinite(x) & np.isfinite(y)

        if not valid.any():
            self.show_message("No valid numeric data available")
            return 
        # remove zoom so when removing a point it doesn't reset the view 
        old_limits = None 
        if keep_view and self.axes.axison: 
            old_limits = (self.axes.get_xlim(),self.axes.get_ylim())
        #stored for click to remove
        self.current_x = x
        self.current_y = y

        self.axes.clear()
        self.axes.set_axis_on()
        self.axes.plot(x,y,linewidth =1.2)

       #turning points removed red 
        if removed_x is not None and len (removed_x )>0:
            self.axes.plot(
                removed_x, removed_y,
                linestyle="none", marker= "x",
                color = "red" , markersize=6,
                label="Removed"
            )
            self.axes.legend(loc="upper left")
        self.axes.set_title(title or variable, fontsize=13, fontweight="bold", pad=20)
        if subtitle:
            self.axes.text(
                0.5, 1.02, subtitle,
                ha="center", va="bottom", fontsize=9, color="#555555",
                transform=self.axes.transAxes
            )
        self.axes.grid(True, color="#dddddd", linewidth=0.8)
        self.axes.set_xlabel(x_label)
        self.axes.set_ylabel(f"{variable} (pixels)")
        if old_limits is not None :
            self.axes.set_xlim(old_limits[0])
            self.axes.set_ylim(old_limits[1])
        self.draw_idle()

    def nearest_point(self, event, max_pixels=20 ):
        """ Index of the plotted point closest to a mouse event, or None """
        x = getattr(self, "current_x", None)
        y = getattr(self, "current_y", None)

        if x is None or y is None or event.x is None:
            return None
        
        valid = np.flatnonzero(np.isfinite(x)& np.isfinite(y))
        if valid.size == 0:
            return None 
        screen = self.axes.transData.transform(
            np.column_stack((x[valid],y[valid]))
        )
        distances = np.hypot(
            screen[:,0]-event.x,
            screen[:,1] - event.y
        )
        closest =int (np.argmin (distances))
        if distances[closest] > max_pixels:
            return None 
        return int(valid [closest])