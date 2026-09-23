# Imports
import pandas as pd # Panda usef for dataset tables

import numpy as np # NumPy performs math calculations
import sys # Python allows system level information interaction

from PySide6.QtCore import Qt # behavior settings used by GUI

from PySide6.QtWidgets import ( # things build GUI with
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

        # Import CSV Button
        self.import_button = QPushButton("Import CSV")

        # Connect CSV button to import function
        self.import_button.clicked.connect(self.import_csv)

        parameter_layout.addWidget(
            self.import_button,
            0, 0, 1, 2,
            Qt.AlignmentFlag.AlignCenter 
        )

        # Space below Import button
        parameter_layout.setRowMinimumHeight(0, 50)

        # Parameter Components
        parameter_title = QLabel("Enter Parameters")
        parameter_layout.setRowMinimumHeight(1, 30)
        parameter_layout.addWidget(
            parameter_title,
            1, 0, 1, 2,
            Qt.AlignmentFlag.AlignCenter
        )

        # Register Paramters Button
        self.parameter_button = QPushButton("Register Parameters")

        # Connect button to function
        self.parameter_button.clicked.connect(self.register_parameters)

        # Put Register button into parameter layout
        parameter_layout.addWidget(
            self.parameter_button,
            9, 0, 1, 2,
            Qt.AlignmentFlag.AlignCenter
        )

        # FPS
        fps_label = QLabel("FPS:")
        self.fps_input = QLineEdit()
        self.fps_input.setPlaceholderText("Enter FPS value:")

        parameter_layout.addWidget(fps_label, 2, 0)
        parameter_layout.addWidget(self.fps_input, 2, 1)

        # Latcal
        latcal_label = QLabel("Latcal (m/pix):")
        self.latcal_input = QLineEdit()
        self.latcal_input.setPlaceholderText("Enter Latcal value:")

        parameter_layout.addWidget(latcal_label, 3, 0)
        parameter_layout.addWidget(self.latcal_input, 3, 1)

        # Dorscal
        dorscal_label = QLabel("Dorscal (m/pix):")
        self.dorscal_input = QLineEdit()
        self.dorscal_input.setPlaceholderText("Enter Dorscal value:")

        parameter_layout.addWidget(dorscal_label, 4, 0)
        parameter_layout.addWidget(self.dorscal_input, 4, 1)

        # Poly 1
        poly1_label = QLabel("Poly 1:")
        self.poly1_input = QLineEdit()
        self.poly1_input.setPlaceholderText("Enter Poly 1 value:")

        parameter_layout.addWidget(poly1_label, 5, 0)
        parameter_layout.addWidget(self.poly1_input, 5, 1)

        # Poly 2
        poly2_label = QLabel("Poly 2:")
        self.poly2_input = QLineEdit()
        self.poly2_input.setPlaceholderText("Enter Poly 2 value:")

        parameter_layout.addWidget(poly2_label, 6, 0)
        parameter_layout.addWidget(self.poly2_input, 6, 1)

        # Poly 3
        poly3_label = QLabel("Poly 3:")
        self.poly3_input = QLineEdit()
        self.poly3_input.setPlaceholderText("Enter Poly 3 value:")

        parameter_layout.addWidget(poly3_label, 7, 0)
        parameter_layout.addWidget(self.poly3_input, 7, 1)

        # TD
        td_label = QLabel("TD:")
        self.td_input = QLineEdit()
        self.td_input.setPlaceholderText("Enter TD value:")

        parameter_layout.addWidget(td_label, 8, 0)
        parameter_layout.addWidget(self.td_input, 8, 1)

        # Register Parameters Button
        self.parameter_button = QPushButton("Register Parameters")

        # Connect Parameter Button to function
        self.parameter_button.clicked.connect(self.register_parameters)

        # Add Register Parameters button to parameter layout
        parameter_layout.addWidget(
            self.parameter_button,
            9, 0, 1, 2,
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

# Import CSV 
    def import_csv(self):

    # Open file picker and allow multiple CSV files
        file_paths, _ = QFileDialog.getOpenFileNames(
        self,
        "Select CSV Files",
        "",
        "CSV Files (*.csv)"
    )

    # Stop if no files were selected
        if not file_paths:
            return

    # Store selected file paths
        self.file_paths = file_paths

    # Store loaded datasets
        self.data = []

    # Load each CSV file with Pandas 
    # Header is set to [0, 1, 2] for scorer, bodypart, coordinates
        for file_path in self.file_paths:
            dataset = pd.read_csv(
                file_path,
                header=[0, 1, 2]
                )
            self.data.append(dataset)

    # Test the first imported dataset
        variables = self.extract_variables(self.data[0])

       # self.calculate_kinematics(variables)

        print("Standardized variables:")
        print(variables.keys())

    # Test output
        print(f"Loaded {len(self.data)} CSV file(s).")

    # Extract one coordinate from a CSV dataset
    def extract_coordinate(self, dataset, bodypart, coordinate):

    # Search the CSV column headers
        for column in dataset.columns:

        # Check body part and coordinate
            if column[1] == bodypart and column[2] == coordinate:

            # Get all values from the matching column
                values = dataset[column]

            # Convert values to numbers and return NumPy array
                return pd.to_numeric(
                    values,
                    errors="coerce"
                ).to_numpy()

    # Coordinate was not found
        return None


# Extract standardized variables for kinematics
    def extract_variables(self, dataset):

        variables = {}

    # Frame number
        variables["frame"] = pd.to_numeric(
            dataset.iloc[:, 0],
            errors="coerce"
        ).to_numpy()

    # Tail tip
        variables["tail_tip_x"] = self.extract_coordinate(
            dataset, "TailTip", "x"
        )

        variables["tail_tip_y"] = self.extract_coordinate(
            dataset, "TailTip", "y"
        )

    # Tail base
        variables["tail_base_x"] = self.extract_coordinate(
            dataset, "TailBase", "x"
        )

        variables["tail_base_y"] = self.extract_coordinate(
            dataset, "TailBase", "y"
        )

    # Snout
        variables["snout_x"] = self.extract_coordinate(
            dataset, "SnoutTip", "x"
        )

        variables["snout_y"] = self.extract_coordinate(
            dataset, "SnoutTip", "y"
        )

    # MTP
        variables["mtp_x"] = self.extract_coordinate(
            dataset, "MTP", "x"
        )

        variables["mtp_y"] = self.extract_coordinate(
            dataset, "MTP", "y"
        )

    # Ankle
        variables["ankle_x"] = self.extract_coordinate(
            dataset, "Ankle", "x"
        )

        variables["ankle_y"] = self.extract_coordinate(
            dataset, "Ankle", "y"
        )

        return variables
    
    
# Formulas Kinematics Calculations

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

    # def calculate_kinematics(self, variables):

        print("\nKINEMATIC RESULTS")
        print("------------------")

    # Convert registered parameter text into numbers
        fps = float(self.fps)
        latcal = float(self.latcal)
        dorscal = float(self.dorscal)
        td = float(self.td)


    # Time
    # Can calculate now because we have frame + FPS
        time = variables["frame"] / fps

        print("Time range:")
        print(f"{time[0]} to {time[-1]} seconds")


    # Swim Velocity
    # Can calculate once we have the correct snout X data
    # and it has gone through the required preprocessing.
    #
    # TODO:
    # Connect processed snout_x from graph/data-processing team.
    #
    # swim_velocity = self.calculate_swim_velocity(
    #     time,
    #     processed_snout_x
    # )


    # Tail Frequency
    # TODO:
    # Requires detected tail-tip peaks from processed graph.
    #
    # Need:
    # - number of waves
    # - first peak time
    # - last peak time
    #
    # tail_frequency = self.calculate_tail_frequency(
    #     number_of_waves,
    #     start_time,
    #     end_time
    # )


    # Tail Wavelength
    # TODO:
    # Requires X positions corresponding to detected
    # tail-tip peaks.
    #
    # tail_wavelength = self.calculate_tail_wavelength(
    #     tail_peak_x_positions
    # )


    # Tail Wave Speed
    # TODO:
    # Requires tail_frequency and tail_wavelength first.
    #
    # wave_speed = self.calculate_wave_speed(
    #     tail_frequency,
    #     tail_wavelength
    # )


    # Tail Tip Amplitude
    # TODO:
    # Requires detected peaks and troughs from
    # the processed tail-tip signal.
    #
    # tail_tip_amplitude = self.calculate_tail_tip_amplitude(
    #     tail_tip_peaks,
    #     tail_tip_troughs
    # )


    # Tail Base Amplitude
    # TODO:
    # Requires detected peaks and troughs from
    # the processed tail-base signal.
    #
    # tail_base_amplitude = self.calculate_tail_base_amplitude(
    #     tail_base_peaks,
    #     tail_base_troughs
    # )


    # Tail Lateral Velocity
    # TODO:
    # Requires tail-tip amplitude and
    # mean peak-to-peak time.
    #
    # tail_lateral_velocity = self.calculate_tail_lateral_velocity(
    #     tail_tip_amplitude,
    #     mean_peak_to_peak_time
    # )


    # Relative Tail Velocity
    # TODO:
    # Requires:
    # - tail lateral velocity
    # - wave speed
    # - swim velocity
    #
    # relative_velocity = self.calculate_relative_velocity(
    #     tail_lateral_velocity,
    #     wave_speed,
    #     swim_velocity
    # )


    # Virtual Mass
    # Can calculate from registered tail diameter
        virtual_mass = self.calculate_virtual_mass(td)

        print(f"Virtual Mass: {virtual_mass}")

        return virtual_mass 

    # Tail Thrust Power
    # TODO:
    # Requires:
    # - virtual mass
    # - relative velocity
    # - swim velocity
    # - tail lateral velocity
    #
    # tail_thrust_power = self.calculate_tail_thrust_power(
    #     virtual_mass,
    #     relative_velocity,
    #     swim_velocity,
    #     tail_lateral_velocity
    # )


    # MTP / Hindfoot Frequency
    # TODO:
    # Requires detected MTP cycles/valleys.
    #
    # mtp_frequency = self.calculate_mtp_frequency(
    #     number_of_cycles,
    #     start_time,
    #     end_time
    # )


    # MTP Amplitude
    # TODO:
    # Requires detected MTP peaks and troughs.
    #
    # mtp_amplitude = self.calculate_mtp_amplitude(
    #     mtp_peaks,
    #     mtp_troughs
    # )


    # MTP Wavelength
    # TODO:
    # Requires X positions corresponding to
    # detected MTP valleys.
    #
    # mtp_wavelength = self.calculate_mtp_wavelength(
    #     mtp_valley_x_positions
    # )


    # Stroke Length
    # TODO:
    # Requires swim_velocity and mtp_frequency.
    #
    # stroke_length = self.calculate_stroke_length(
    #     swim_velocity,
    #     mtp_frequency
    # )


    # Power Phase Duration
    # TODO:
    # Requires MTP peak/valley timing from processed signal.
    #
    # power_duration = self.calculate_power_phase_duration(
    #     peak_times,
    #     valley_times
    # )


    # Recovery Phase Duration
    # TODO:
    # Requires MTP peak/valley timing from processed signal.
    #
    # recovery_duration = self.calculate_recovery_phase_duration(
    #     next_peak_times,
    #     valley_times
    # )


    # Power / Recovery Ratio
    # TODO:
    # Requires power_duration and recovery_duration.
    #
    # phase_ratio = self.calculate_phase_ratio(
    #     power_duration,
    #     recovery_duration
    # )


    # Hindfoot Length
    # TODO:
    # Formula is implemented, but use the processed/calibrated
    # MTP and ankle coordinates before calculating the final metric.
    #
    # hindfoot_length = self.calculate_hindfoot_length(
    #     processed_mtp_x,
    #     processed_mtp_y,
    #     processed_ankle_x,
    #     processed_ankle_y
    # )


    # Hindfoot Angle
    # TODO:
    # Use processed/calibrated MTP and ankle coordinates.
    #
    # hindfoot_angle = self.calculate_hindfoot_angle(
    #     processed_mtp_x,
    #     processed_mtp_y,
    #     processed_ankle_x,
    #     processed_ankle_y
    # )


    # Hindfoot Angular Velocity
    # TODO:
    # Requires hindfoot_angle + corresponding processed time.
    #
    # angular_velocity = self.calculate_hindfoot_angular_velocity(
    #     hindfoot_angle,
    #     time
    # )

# Start application
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())