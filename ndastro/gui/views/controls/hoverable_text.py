"""Module to hold hoverable text item."""

from __future__ import annotations

from typing import cast

from PySide6.QtCore import QPoint, QRect, QSize
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsTextItem,
    QWidget,
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

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Fire when the mouse enters the text.

        Args:
            event (QGraphicsSceneHoverEvent): _description_

        """
        # Create and show the popup
        if not self.popup:
            self.popup = CustomPopup(self.toPlainText(), None)

        self.show_smart_popup(event.screenPos())

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Fire when the mouse leaves the text.

        Args:
            event (_type_): _description_

        """
        super().hoverLeaveEvent(event)

    def hide_popup(self) -> None:
        """Hide the popup."""
        if isinstance(self.popup, CustomPopup) and not self.popup.mouse_inside:
            self.popup.hide()

    def show_smart_popup(self, hover_pos: QPoint) -> None:
        """Show the popup at below hovered position.

        Args:
            hover_pos (QPoint): The position of the mouse hover in global coordinates.

        """
        popup = cast("QWidget", self.popup)
        popup.adjustSize()
        popup_size = popup.size()

        button_pos_global = hover_pos
        screen_geo = QApplication.primaryScreen().availableGeometry()
        window_geo = self._get_window_geometry()

        popup_pos = self._calculate_popup_position(
            button_pos_global,
            popup_size,
            window_geo,
            screen_geo,
        )

        popup.move(popup_pos)
        popup.show()

    def _get_window_geometry(self) -> QRect:
        """Get the geometry of the window in global coordinates."""
        view = self.scene().views()[0]
        window_geo = view.frameGeometry()
        window_geo.moveTopLeft(view.mapToGlobal(QPoint(0, 0)))
        return window_geo

    def _calculate_popup_position(
        self,
        button_pos: QPoint,
        popup_size: QSize,
        window_geo: QRect,
        screen_geo: QRect,
    ) -> QPoint:
        """Calculate the optimal position for the popup.

        Args:
            button_pos (QPoint): The position of the button in global coordinates.
            popup_size (QSize): The size of the popup.
            window_geo (QRect): The geometry of the window.
            screen_geo (QRect): The geometry of the screen.

        Returns:
            QPoint: The calculated position for the popup.

        """
        popup_pos = button_pos + QPoint(0, 0)

        # Check window boundaries
        popup_pos = self._adjust_for_window_boundaries(
            popup_pos,
            popup_size,
            button_pos,
            window_geo,
        )

        # Check screen boundaries
        return self._adjust_for_screen_boundaries(popup_pos, popup_size, screen_geo)

    def _adjust_for_window_boundaries(
        self,
        popup_pos: QPoint,
        popup_size: QSize,
        button_pos: QPoint,
        window_geo: QRect,
    ) -> QPoint:
        """Adjust the popup position to fit within the window boundaries."""
        if popup_pos.x() + popup_size.width() > window_geo.right():
            left_pos = button_pos - QPoint(popup_size.width(), 0)
            popup_pos.setX(
                left_pos.x() if left_pos.x() >= window_geo.left() else window_geo.right() - popup_size.width(),
            )

        if popup_pos.x() < window_geo.left():
            right_pos = button_pos + QPoint(0, 0)
            popup_pos.setX(
                right_pos.x() if right_pos.x() + popup_size.width() <= window_geo.right() else window_geo.left(),
            )

        if popup_pos.y() + popup_size.height() > window_geo.bottom():
            above_pos = button_pos - QPoint(0, popup_size.height())
            popup_pos.setY(
                above_pos.y() if above_pos.y() >= window_geo.top() else window_geo.bottom() - popup_size.height(),
            )

        return popup_pos

    def _adjust_for_screen_boundaries(
        self,
        popup_pos: QPoint,
        popup_size: QSize,
        screen_geo: QRect,
    ) -> QPoint:
        """Adjust the popup position to fit within the screen boundaries."""
        if popup_pos.x() + popup_size.width() > screen_geo.right():
            popup_pos.setX(screen_geo.right() - popup_size.width())

        if popup_pos.x() < screen_geo.left():
            popup_pos.setX(screen_geo.left())

        if popup_pos.y() + popup_size.height() > screen_geo.bottom():
            popup_pos.setY(screen_geo.bottom() - popup_size.height())

        if popup_pos.y() < screen_geo.top():
            popup_pos.setY(screen_geo.top())

        return popup_pos
