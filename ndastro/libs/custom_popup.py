"""Module to hold custom popup."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from PySide6.QtGui import QEnterEvent


class CustomPopup(QWidget):
    """The custom popup.

    Args:
        QWidget (_type_): _description_

    """

    def __init__(self, text: str, parent: QWidget | None) -> None:
        """Initialize the custom popup.

        Args:
            text (_type_): _description_
            parent (_type_, optional): _description_. Defaults to None.

        """
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.ToolTip)  # Make it a lightweight popup

        # Add elements to the popup
        label = QLabel(f"Details for: {text}")
        label.setStyleSheet("font-weight: bold;")
        button = QPushButton("Click Me")

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)

        self.mouse_inside = False  # Track mouse presence

    def enterEvent(self, event: QEnterEvent) -> None:
        """Fire when the mouse enters the popup."""
        self.mouse_inside = True
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Fire when the mouse leaves the popup."""
        self.mouse_inside = False
        self.hide()
        super().leaveEvent(event)
