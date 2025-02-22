from __future__ import annotations

from typing import TYPE_CHECKING, cast

from i18n import t
from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView

from ndastro.libs.hoverable_text import HoverableTextItem

if TYPE_CHECKING:
    from PySide6.QtGui import QResizeEvent

    from ndastro.gui.viewmodels.ndastro_viewmodel import NDAstroViewModel


type SceneItem = dict[str, QGraphicsRectItem | HoverableTextItem]


class ResizableAstroChart(QGraphicsView):
    """Resizable astro chart.

    Args:
        QGraphicsView (_type_): _description_

    """

    def __init__(self, view_model: NDAstroViewModel) -> None:
        """Resizable astro chart."""
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.rects: list[list[SceneItem | None]] = [[{} for i in range(4)] for j in range(4)]  # Store references to the rectangles
        self._view_model = view_model
        self._view_model.language_changed.connect(self._retranslate_ui)
        self.box_rasi_map = [12, 1, 2, 3, 11, 4, 10, 5, 9, 8, 7, 6]
        self.init_scene()

    def init_scene(self) -> None:
        """Create and add rects to the scene."""
        # Draw the 4x4 grid
        square_size = 200  # 15 cm = 150 mm (scaled by 10 for simplicity)

        count = 1
        for row in range(4):
            for col in range(4):
                if (row, col) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
                    continue
                x = col * square_size
                y = row * square_size

                # Create a square with a visible fill color
                rect = QGraphicsRectItem(x, y, square_size, square_size)

                # Add a text label inside the square
                text = HoverableTextItem(t(f"core.rasis.rasi{self.box_rasi_map[count - 1]}"), None)
                text.setParentItem(rect)  # Set rect as the parent
                text.setPos(
                    x + square_size / 4,
                    y + square_size / 4,
                )  # Position inside the square

                self.scene().addItem(rect)

                self.rects[row][col] = {"rect": rect, "text": text}

                count += 1

        self.update_rects()  # Initial position and size adjustment

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Fire when the view is resized."""
        super().resizeEvent(event)
        self.update_scene_size()
        self.update_rects()

    def update_scene_size(self) -> None:
        """Update the scene size to match the view size."""
        self.scene().setSceneRect(
            0,
            0,
            self.viewport().width(),
            self.viewport().height(),
        )

    def update_rects(self) -> None:
        """Resize and reposition rectangles based on the view size."""
        view_width = self.viewport().width()
        view_height = self.viewport().height()

        # Example: evenly distribute the rectangles in the scene
        rect_width = (view_width) / 4  # 4 rects in a row
        rect_height = view_height / 4

        count = 1
        for row in range(4):
            for col in range(4):
                if (row, col) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
                    continue
                x = col * rect_width
                y = row * rect_height

                dic = cast(SceneItem, self.rects[row][col])
                if dic is not None and len(dic) == 2:
                    rect = cast(QGraphicsRectItem, dic["rect"])
                    rect.setRect(
                        QRectF(x, y, rect_width, rect_height),
                    )  # Update size and position

                    text = cast(HoverableTextItem, dic["text"])
                    text.setPos(x + rect_width / 4, y + rect_height / 4)
                    text.setPlainText(t(f"core.rasis.rasi{self.box_rasi_map[count - 1]}"))

                count += 1

    def _retranslate_ui(self) -> None:
        self.update_rects()
