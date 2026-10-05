# Imports

import sys

from pathlib import Path

from PySide6.QtWidgets import QApplication

from gui import MainWindow


# Create application

app = QApplication(sys.argv)


# Load GUI stylesheet

style_path = Path(__file__).with_name(
    "styles.qss"
)

if style_path.exists():

    with open(
        style_path,
        "r"
    ) as style_file:

        app.setStyleSheet(
            style_file.read()
        )


# Create main window

window = MainWindow()

window.show()


# Start application

sys.exit(
    app.exec()
)