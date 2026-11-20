"""Application entry point for the MiceLab desktop client."""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from gui import MainWindow


def main():
    """Create the Qt application, load its stylesheet, and show the main window."""
    app = QApplication(sys.argv)
    style_path = Path(__file__).with_name("styles.qss")
    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
