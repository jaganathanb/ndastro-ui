from typing import cast

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QResizeEvent
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView

from ndastro.libs.hoverable_text import HoverableTextItem

type SceneItem = dict[str, QGraphicsRectItem | HoverableTextItem]


class ResizableAstroChart(QGraphicsView):
    """Resizable astro chart.

    Args:
        QGraphicsView (_type_): _description_

    """

    def __init__(self) -> None:
        """Resizable astro chart."""
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.rects: list[list[SceneItem | None]] = [[{} for i in range(4)] for j in range(4)]  # Store references to the rectangles
        self.init_scene()

    def init_scene(self) -> None:
        """Create and add rects to the scene."""
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(2)

        # Draw the 4x4 grid
        square_size = 200  # 15 cm = 150 mm (scaled by 10 for simplicity)

        for row in range(4):
            for col in range(4):
                if (row, col) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
                    continue
                x = col * square_size
                y = row * square_size

                # Create a square with a visible fill color
                rect = QGraphicsRectItem(x, y, square_size, square_size)
                rect.setPen(pen)
                rect.setBrush(QBrush(Qt.GlobalColor.white))

                # Add a text label inside the square
                text = HoverableTextItem(f"({row},{col})", None)
                text.setFont(QFont("Arial", 14))
                text.setDefaultTextColor(QColor(Qt.GlobalColor.blue))
                text.setParentItem(rect)  # Set rect as the parent
                text.setPos(
                    x + square_size / 4,
                    y + square_size / 4,
                )  # Position inside the square

                self.scene().addItem(rect)

                self.rects[row][col] = {"rect": rect, "text": text}

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

        for row in range(4):
            for col in range(4):
                if (row, col) in [(1, 1), (1, 2), (2, 1), (2, 2)]:
                    continue
                x = col * rect_width
                y = row * rect_height

                dic = cast(SceneItem, self.rects[row][col])
                rect = cast(QGraphicsRectItem, dic["rect"])
                rect.setRect(
                    QRectF(x, y, rect_width, rect_height),
                )  # Update size and position

                text = cast(HoverableTextItem, dic["text"])
                text.setPos(x + rect_width / 4, y + rect_height / 4)
