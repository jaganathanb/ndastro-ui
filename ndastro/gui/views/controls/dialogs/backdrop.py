"""Define the Backdrop class, a semi-transparent widget.

Used as a backdrop behind modal dialogs in the application.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget


class Backdrop(QWidget):
    """Semi-transparent backdrop behind the modal dialog."""

    def __init__(self, parent: QWidget) -> None:
        """Initialize the Backdrop widget.

        Args:
            parent (QWidget): The parent widget for this backdrop.

        """
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog,
        )
        self.setAutoFillBackground(False)
        self.setWindowOpacity(0.75)
        self.setStyleSheet("background-color: grey;")  # Semi-transparent black
        self.setGeometry(parent.geometry())
        self.show()
