# Imports
import sys

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout, 
    QWidget,
)


# GUI
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("MiceLab")
        self.resize(800, 600)

        # Main container
        main_container = QWidget()
        self.setCentralWidget(main_container)

        # Main layout
        main_layout = QVBoxLayout()
        main_container.setLayout(main_layout)

        # Parameter container
        parameter_container = QWidget()

        # Parameter layout
        parameter_layout = QGridLayout(parameter_container)
        parameter_layout.setVerticalSpacing(0)
        parameter_layout.setHorizontalSpacing(0)

        # Space around layout edges
        parameter_container.setContentsMargins(0, 0, 0, 0)
        parameter_container.setLayout(parameter_layout)
      


        # Parameter Components
        parameter_title = QLabel("Enter Parameters")

       
        

        # FPS
        fps_label = QLabel("FPS:")
        fps_input = QLineEdit()
        fps_input.setPlaceholderText("Enter FPS value:")

        parameter_layout.addWidget(
            parameter_title,
            0, 0, 1, 2,
            Qt.AlignmentFlag.AlignCenter
        )
        parameter_layout.addWidget(fps_label, 1, 0)
        parameter_layout.addWidget(fps_input, 1, 1)

        # Import CSV button

        # Latcal
        latcal_label = QLabel("Latcal (m/pix):")
        latcal_input = QLineEdit()
        latcal_input.setPlaceholderText("Enter Latcal value:")

        parameter_layout.addWidget(latcal_label, 2, 0)
        parameter_layout.addWidget(latcal_input, 2, 1)

        # Dorscal 
        dorscal_label = QLabel("Dorscal (m/pix):")
        dorscal_input = QLineEdit()
        dorscal_input.setPlaceholderText("Enter Dorscal value:")

        parameter_layout.addWidget(dorscal_label, 3, 0)
        parameter_layout.addWidget(dorscal_input, 3, 1)

        # Poly 1
        poly1_label = QLabel("Poly 1:")
        poly1_input = QLineEdit()
        poly1_input.setPlaceholderText("Enter Poly 1 value:")

        parameter_layout.addWidget(poly1_label, 4, 0)
        parameter_layout.addWidget(poly1_input, 4, 1)

        # Poly 2
        poly2_label = QLabel("Poly 2:")
        poly2_input = QLineEdit()
        poly2_input.setPlaceholderText("Enter Poly 2 value:")

        parameter_layout.addWidget(poly2_label, 5, 0)
        parameter_layout.addWidget(poly2_input, 5, 1)

        # Poly 3
        poly3_label = QLabel("Poly 3:")
        poly3_input = QLineEdit()
        poly3_input.setPlaceholderText("Enter Poly 3 value:")

        parameter_layout.addWidget(poly3_label, 6, 0)
        parameter_layout.addWidget(poly3_input, 6, 1)

        # TD
        td_label = QLabel("TD:")
        td_input = QLineEdit()
        td_input.setPlaceholderText("Enter TD value:")

        parameter_layout.addWidget(td_label, 7, 0)
        parameter_layout.addWidget(td_input, 7, 1)


        # Put parameter container into main layout
        main_layout.addWidget(
            parameter_container,
            alignment=Qt.AlignmentFlag.AlignTop
            )



# Start application
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())