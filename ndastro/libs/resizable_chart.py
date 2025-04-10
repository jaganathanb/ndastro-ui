from __future__ import annotations

from typing import TYPE_CHECKING, cast

from i18n import t
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QFont, QPen
from PySide6.QtWidgets import (
    QGraphicsLineItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
)

from ndastro.libs.hoverable_text import HoverableTextItem
from ndastro.libs.planet_enum import Planets

if TYPE_CHECKING:
    from PySide6.QtGui import QResizeEvent
    from skyfield.units import Angle

    from ndastro.gui.models.planet_position import PlanetDetail
    from ndastro.gui.viewmodels.ndastro_viewmodel import NDAstroViewModel

from ndastro.libs.constants import KATTAM_RASI_MAP, SYMBOLS


class ResizableAstroChart(QGraphicsView):
    """Resizable astro chart.

    Args:
        QGraphicsView (_type_): _description_

    """

    def __init__(self, view_model: NDAstroViewModel) -> None:
        """Resizable astro chart."""
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self._view_model = view_model
        self.theme = view_model.settings.get("theme")
        self._view_model.language_changed.connect(self._retranslate_ui)
        self._view_model.theme_changed.connect(self._update_theme)

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
                brush = QBrush(Qt.GlobalColor.gray)
                pen = QPen(brush, 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap)
                pen.setWidth(1)

                rect.setPen(pen)

                # Add a text label inside the square
                kattam = self._view_model.kattams[KATTAM_RASI_MAP[count - 1] - 1] if self._view_model.kattams else None
                text = HoverableTextItem(str(kattam.house.value) if kattam else "", None)
                text.setDefaultTextColor(Qt.GlobalColor.black if self.theme == "light" else Qt.GlobalColor.white)
                text.setScale(1.5)

                width = rect.rect().width()
                height = rect.rect().height()

                if kattam and kattam.planets:
                    sorted_planets = sorted(kattam.planets, key=lambda p: cast("float", cast("Angle", p.advanced_by).degrees))
                    for i, planet in enumerate(sorted_planets):
                        planet_name = QGraphicsTextItem()
                        font = QFont()
                        font.setBold(True)
                        planet_name.setFont(font)
                        planet_name.setHtml(
                            f"<span>{planet.short_name}<sub>{SYMBOLS.RETROGRADE_SYMBOL if planet.retrograde else ''}</sub></span>",
                        )
                        planet_name.setData(1, planet)
                        planet_name.setParentItem(rect)

                        # Calculate position based on the rect x and sorted planet longitudes
                        planet_x = x + ((cast("float", cast("Angle", planet.advanced_by).degrees) / 30) * (width - (width * 0.15)))
                        planet_y = y + (0 if i % 2 == 0 else planet_name.boundingRect().height())
                        planet_name.setPos(planet_x, planet_y)

                if kattam is not None and kattam.is_ascendant is True:
                    self.draw_lagna_lines(row, col, rect)

                text.setParentItem(rect)  # Set rect as the parent

                text.setPos(
                    (col * width - 15)  # no of kattams already plotted left to right - some gap
                    + width  # + the width of the current kattam
                    - text.boundingRect().width(),  # - text width
                    (row * height) + 30 - text.boundingRect().height(),  # no of kattams already plotted top to bottom - some gap - text height
                )  # Position inside the square

                self.scene().addItem(rect)

                count += 1

        self.update_rects()

    def draw_lagna_lines(self, row: int, col: int, rect: QGraphicsRectItem) -> None:
        """Draw lagna lines on the specified rectangle."""
        bound = cast("QGraphicsRectItem", rect).boundingRect()
        lx = abs(bound.x() * col)
        ly = abs(bound.y() * row)
        line1 = QGraphicsLineItem(lx + 3, ly + bound.height() * 0.20, lx + bound.width() * 0.20, ly + 3)
        line1.setData(1, "first")
        line1.setPen(QPen(Qt.GlobalColor.red, 2))
        line1.setParentItem(rect)

        line2 = QGraphicsLineItem(lx + 3, ly + bound.height() * 0.22, lx + bound.width() * 0.22, ly + 3)
        line2.setData(1, "second")
        line2.setPen(QPen(Qt.GlobalColor.red, 2))
        line2.setParentItem(rect)  # Initial position and size adjustment

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
        view_width = self.viewport().width() - 1
        view_height = self.viewport().height() - 1

        # Example: evenly distribute the rectangles in the scene
        rect_width = view_width / 4  # 4 rects in a row
        rect_height = view_height / 4

        for item in self.scene().items():
            if isinstance(item, QGraphicsRectItem):
                x = item.rect().x() // item.rect().width() * rect_width
                y = item.rect().y() // item.rect().height() * rect_height
                item.setRect(QRectF(x, y, rect_width, rect_height))

                width = item.rect().width()
                height = item.rect().height()

                for child in item.childItems():
                    if isinstance(child, HoverableTextItem):
                        child.setDefaultTextColor(Qt.GlobalColor.black if self.theme == "light" else Qt.GlobalColor.white)
                        child.setPos(
                            (x + rect_width - child.boundingRect().width() - 15),
                            (y + 30 - child.boundingRect().height()),
                        )
                    elif isinstance(child, QGraphicsLineItem):
                        line = child

                        if line.data(1) == "first":
                            line.setLine(x + 3, y + item.boundingRect().height() * 0.20, x + item.boundingRect().width() * 0.20, y + 3)
                        else:
                            line.setLine(x + 3, y + item.boundingRect().height() * 0.22, x + item.boundingRect().width() * 0.22, y + 3)

                # Get all QGraphicsTextItem from item.childItems()
                planet_names = [child for child in item.childItems() if isinstance(child, QGraphicsTextItem)]
                for i, planet_name in enumerate(planet_names):
                    planet = cast("PlanetDetail", planet_name.data(1))
                    if planet:
                        # Calculate position based on the rect x and sorted planet longitudes
                        t_width = planet_name.boundingRect().width()  # text width
                        t_height = planet_name.boundingRect().height()  # text height
                        per_width = (
                            cast("float", cast("Angle", planet.advanced_by).degrees) / 30
                        ) * width  # position based on the rect x and sorted planet longitudes
                        actual_pos = x + per_width + t_width  # planet position in the rect + text width
                        if_a_crosses_rect = actual_pos > (x + width)  # if planet crosses the rect
                        planet_x = x + per_width - (actual_pos - (x + width) if if_a_crosses_rect else 0)  # planet position in the rect
                        planet_y = y + height / 3 + (0 if i % 2 == 0 else t_height)

                        font = QFont()
                        font.setBold(True)
                        font.setPixelSize(20)
                        planet_name.setFont(font)
                        planet_name.setDefaultTextColor(Qt.GlobalColor.black if self.theme == "light" else Qt.GlobalColor.white)
                        planet_name.setHtml(
                            f"<span>{t('core.raising_sign')[:3] if planet.is_ascendant else t(f'core.planets.planet{planet.planet.value}')[:2]} \
                                <sub> \
                                {
                                SYMBOLS.RETROGRADE_SYMBOL
                                if planet.retrograde and planet.planet.code not in [Planets.RAHU.code, Planets.KETHU.code]
                                else ''
                            }</sub></span>",
                        )
                        planet_name.setPos(
                            planet_x,
                            planet_y,
                        )

    def _retranslate_ui(self) -> None:
        self.update_rects()

    def _update_theme(self, theme: str) -> None:
        """Update the theme of the chart."""
        # Add logic to update the theme, e.g., changing colors or styles
        self.theme = theme
        self.update_rects()
