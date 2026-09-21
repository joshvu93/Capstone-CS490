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
    QPushButton,
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

        parameter_layout.addWidget(
            parameter_title,
            0, 0, 1, 2,
            Qt.AlignmentFlag.AlignCenter
        )

        # Import CSV button
        # We will add this later

        # FPS
        fps_label = QLabel("FPS:")
        self.fps_input = QLineEdit()
        self.fps_input.setPlaceholderText("Enter FPS value:")

        parameter_layout.addWidget(fps_label, 1, 0)
        parameter_layout.addWidget(self.fps_input, 1, 1)

        # Latcal
        latcal_label = QLabel("Latcal (m/pix):")
        self.latcal_input = QLineEdit()
        self.latcal_input.setPlaceholderText("Enter Latcal value:")

        parameter_layout.addWidget(latcal_label, 2, 0)
        parameter_layout.addWidget(self.latcal_input, 2, 1)

        # Dorscal
        dorscal_label = QLabel("Dorscal (m/pix):")
        self.dorscal_input = QLineEdit()
        self.dorscal_input.setPlaceholderText("Enter Dorscal value:")

        parameter_layout.addWidget(dorscal_label, 3, 0)
        parameter_layout.addWidget(self.dorscal_input, 3, 1)

        # Poly 1
        poly1_label = QLabel("Poly 1:")
        self.poly1_input = QLineEdit()
        self.poly1_input.setPlaceholderText("Enter Poly 1 value:")

        parameter_layout.addWidget(poly1_label, 4, 0)
        parameter_layout.addWidget(self.poly1_input, 4, 1)

        # Poly 2
        poly2_label = QLabel("Poly 2:")
        self.poly2_input = QLineEdit()
        self.poly2_input.setPlaceholderText("Enter Poly 2 value:")

        parameter_layout.addWidget(poly2_label, 5, 0)
        parameter_layout.addWidget(self.poly2_input, 5, 1)

        # Poly 3
        poly3_label = QLabel("Poly 3:")
        self.poly3_input = QLineEdit()
        self.poly3_input.setPlaceholderText("Enter Poly 3 value:")

        parameter_layout.addWidget(poly3_label, 6, 0)
        parameter_layout.addWidget(self.poly3_input, 6, 1)

        # TD
        td_label = QLabel("TD:")
        self.td_input = QLineEdit()
        self.td_input.setPlaceholderText("Enter TD value:")

        parameter_layout.addWidget(td_label, 7, 0)
        parameter_layout.addWidget(self.td_input, 7, 1)

        # Register Parameters Button
        self.parameter_button = QPushButton("Register Parameters")

        # Connect Parameter Button to function
        self.parameter_button.clicked.connect(self.register_parameters)

        # Add Register Parameters button to parameter layout
        parameter_layout.addWidget(
            self.parameter_button,
            8, 0, 1, 2,
            Qt.AlignmentFlag.AlignCenter
        )

        # Put parameter container into main layout
        main_layout.addWidget(
            parameter_container,
            alignment=Qt.AlignmentFlag.AlignTop
        )


    def register_parameters(self):
        self.fps = self.fps_input.text()
        self.latcal = self.latcal_input.text()
        self.dorscal = self.dorscal_input.text()
        self.poly1 = self.poly1_input.text()
        self.poly2 = self.poly2_input.text()
        self.poly3 = self.poly3_input.text()
        self.td = self.td_input.text()

        print("Parameters registered:")
        print(f"FPS: {self.fps}")
        print(f"Latcal: {self.latcal}")
        print(f"Dorscal: {self.dorscal}")
        print(f"Poly 1: {self.poly1}")
        print(f"Poly 2: {self.poly2}")
        print(f"Poly 3: {self.poly3}")
        print(f"TD: {self.td}")


# Start application
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())