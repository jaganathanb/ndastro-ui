"""Module to hold hoverable text item."""

from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsTextItem,
)

from ndastro.libs.custom_popup import CustomPopup


class HoverableTextItem(QGraphicsTextItem):
    """The hoverable text.

    Args:
        QGraphicsTextItem (_type_): _description_

    """

    def __init__(self, text: str, parent: QGraphicsItem | None) -> None:
        """Initialize the hoverable text.

        Args:
            text (str): text of the element
            parent (QGraphicsItem): _description_

        """
        super().__init__(text, parent)
        self.setAcceptHoverEvents(True)  # Enable hover events
        self.popup: CustomPopup | None = None

        self.hide_timer = QTimer()  # Timer for delayed hide
        self.hide_timer.setSingleShot(True)  # One-shot timer
        self.hide_timer.timeout.connect(self.hide_popup)  # Connect timeout to hide

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Fire when the mouse enters the text.

        Args:
            event (QGraphicsSceneHoverEvent): _description_

        """
        # Create and show the popup
        if not self.popup:
            self.popup = CustomPopup(self.toPlainText(), None)

        self.popup.move(event.screenPos().x() + 10, event.screenPos().y() + 10)
        self.popup.show()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Fire when the mouse leaves the text.

        Args:
            event (_type_): _description_

        """
        self.hide_timer.start(500)  # Set a 500ms delay before hiding
        super().hoverLeaveEvent(event)

    def hide_popup(self) -> None:
        """Hide the popup."""
        if isinstance(self.popup, CustomPopup) and not self.popup.mouse_inside:
            self.popup.hide()
