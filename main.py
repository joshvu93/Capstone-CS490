# Imports
import numpy as np
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

    # Function to register parameters
    def register_parameters(self):
        self.fps = self.fps_input.text()
        self.latcal = self.latcal_input.text()
        self.dorscal = self.dorscal_input.text()
        self.poly1 = self.poly1_input.text()
        self.poly2 = self.poly2_input.text()
        self.poly3 = self.poly3_input.text()
        self.td = self.td_input.text()

        # Console to confirm parameters have been registered
        print("Parameters registered:")
        print(f"FPS: {self.fps}")
        print(f"Latcal: {self.latcal}")
        print(f"Dorscal: {self.dorscal}")
        print(f"Poly 1: {self.poly1}")
        print(f"Poly 2: {self.poly2}")
        print(f"Poly 3: {self.poly3}")
        print(f"TD: {self.td}")

# Formulas Kinematics Calculations

# Kinematic Calculations

# Convert frame number to time in seconds
# Formula: time = frame / fps
def calculate_time(self, frame, fps):
    return frame / fps

# Tail-tip frequency
# Formula: frequency = number of waves / elapsed time
def calculate_tail_frequency(
    self,
    number_of_waves,
    start_time,
    end_time
):
    elapsed_time = end_time - start_time

    return number_of_waves / elapsed_time

# Tail-tip wavelength
# Formula: mean distance between consecutive peak X positions
def calculate_tail_wavelength(
    self,
    peak_x_positions
):
    differences = np.diff(peak_x_positions)

    return np.mean(differences)

# Tail wave speed
# Formula: wave speed = frequency * wavelength
def calculate_wave_speed(
    self,
    frequency,
    wavelength
):
    return frequency * wavelength

# Swimming velocity
# Formula: slope of snout X position over time
def calculate_swim_velocity(
    self,
    time,
    snout_x
):
    slope, intercept = np.polyfit(
        time,
        snout_x,
        1
    )

    return slope

# Tail-tip amplitude
# Formula: mean(peak - trough) / 2
def calculate_tail_tip_amplitude(
    self,
    peaks,
    troughs
):
    return np.mean(peaks - troughs) / 2

# Tail-base amplitude
# Formula: mean(peak - trough) / 2
def calculate_tail_base_amplitude(
    self,
    peaks,
    troughs
):
    return np.mean(peaks - troughs) / 2

# Tail lateral velocity
# Formula:
# (4 * tail-tip amplitude) / mean peak-to-peak time
def calculate_tail_lateral_velocity(
    self,
    tail_tip_amplitude,
    mean_peak_to_peak_time
):
    return (
        4 * tail_tip_amplitude
    ) / mean_peak_to_peak_time

# Relative tail velocity
# Formula:
# lateral velocity *
# ((wave speed - swim velocity) / wave speed)
def calculate_relative_velocity(
    self,
    lateral_velocity,
    wave_speed,
    swim_velocity
):
    return lateral_velocity * (
        (wave_speed - swim_velocity)
        / wave_speed
    )

# Virtual mass
# Formula:
# 1000 * (tail diameter ^2 / 4)
def calculate_virtual_mass(
    self,
    tail_diameter
):
    return 1000 * (
        tail_diameter ** 2 / 4
    )

# Mean tail thrust power
def calculate_tail_thrust_power(
    self,
    virtual_mass,
    relative_velocity,
    swim_velocity,
    lateral_velocity
):
    return (
        virtual_mass
        * relative_velocity
        * swim_velocity
        * lateral_velocity
    )   - (
        0.5
        * virtual_mass
        * relative_velocity ** 2
        * swim_velocity
    )

# MTP / hindfoot frequency
# Formula:
# number of cycles / elapsed time
def calculate_mtp_frequency(
    self,
    number_of_cycles,
    start_time,
    end_time
):
    elapsed_time = end_time - start_time

    return number_of_cycles / elapsed_time

# MTP amplitude
# Formula:
# mean(peak - trough) / 2
def calculate_mtp_amplitude(
    self,
    peaks,
    troughs
):
    return np.mean(peaks - troughs) / 2

# MTP wavelength
# Formula:
# mean distance between consecutive valley X positions
def calculate_mtp_wavelength(
    self,
    valley_x_positions
):
    differences = np.diff(
        valley_x_positions
    )

    return np.mean(differences)

# Hindfoot stroke length
# Formula:
# swim velocity / MTP frequency
def calculate_stroke_length(
    self,
    swim_velocity,
    mtp_frequency
):
    return (
        swim_velocity
        / mtp_frequency
    )

# Power-phase duration
# Formula:
# mean(valley time - peak time)
def calculate_power_phase_duration(
    self,
    peak_times,
    valley_times
):
    return np.mean(
        valley_times - peak_times
    )

# Recovery-phase duration
# Formula:
# mean(next peak time - valley time)
def calculate_recovery_phase_duration(
    self,
    next_peak_times,
    valley_times
):
    return np.mean(
        next_peak_times - valley_times
    )

# Power / recovery phase ratio
# Formula:
# power duration / recovery duration
def calculate_phase_ratio(
    self,
    power_duration,
    recovery_duration
):
    return (
        power_duration
        / recovery_duration
    )

# Hindfoot length
# Formula:
# sqrt((MTPx - Anklex)^2 + (MTPy - Ankley)^2)
def calculate_hindfoot_length(
    self,
    mtp_x,
    mtp_y,
    ankle_x,
    ankle_y
):
    distances = np.sqrt(
        (mtp_x - ankle_x) ** 2
        +
        (mtp_y - ankle_y) ** 2
    )

    return np.mean(distances)

# Hindfoot angle
# Formula:
# atan2(MTPy - Ankley, MTPx - Anklex)
def calculate_hindfoot_angle(
    self,
    mtp_x,
    mtp_y,
    ankle_x,
    ankle_y
):
    return np.arctan2(
        mtp_y - ankle_y,
        mtp_x - ankle_x
    )

# Hindfoot angular velocity
# Formula:
# change in angle / change in time
def calculate_hindfoot_angular_velocity(
    self,
    angle,
    time
):
    return (
        np.diff(angle)
        /
        np.diff(time)
    )

# Start application
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())