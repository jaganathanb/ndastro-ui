from __future__ import annotations

from typing import cast

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ndastro.gui.views.controls.dialogs.backdrop import Backdrop


class FramelessModalDialog(QDialog):
    """A frameless modal dialog with optional title, content, and close button.

    This dialog is designed to be displayed without a window frame and can optionally
    include a backdrop when shown. It supports customizable title, content, and a close
    button for user interaction.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        title: str | None = None,
        content: QWidget | None = None,
    ) -> None:
        """Initialize a frameless modal dialog.

        Args:
            parent (QWidget | None): The parent widget of the dialog.
            title (str | None): The title of the dialog.
            content (QWidget | None): The content widget to display inside the dialog.
            show_close_button (bool): Whether to show a close button in the dialog.

        """
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)

        self.setStyleSheet("""
                 border-radius: 4px;
        """)

        self._backdrop = None
        self._title = title
        self._content = content

        self._setup_ui()

    def _setup_ui(self) -> None:
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 20, 20, 20)

        container = QWidget()

        inner_layout = QVBoxLayout(container)

        if self._title:
            title_label = QLabel(self._title)
            inner_layout.addWidget(title_label)

        if self._content:
            inner_layout.addWidget(self._content)

        outer_layout.addWidget(container)

    def show_with_backdrop(self) -> None:
        """Display the dialog with a backdrop behind it.

        This method creates a backdrop for the dialog if it has a parent,
        centers the dialog on the parent, and then executes the dialog.
        The backdrop is closed once the dialog is dismissed.
        """
        if self.parent():
            self._backdrop = Backdrop(cast("QWidget", self.parent()))
            self._center_dialog()
        self.exec()
        if self._backdrop:
            self._backdrop.close()

    def _center_dialog(self) -> None:
        if self.parent():
            parent_rect = cast("QWidget", self.parent()).rect()
            self.resize(
                int(parent_rect.width() * 0.75),
                int(parent_rect.height() * 0.75),
            )
            dialog_width = self.width()
            dialog_height = self.height()

            bd = cast("QWidget", self._backdrop)

            self.move(
                bd.x() + (bd.width() // 2 - dialog_width // 2),
                bd.y() + (bd.height() // 2 - dialog_height // 2),
            )  # Center the dialog
        else:
            # If no parent, resize to 75% of the screen
            screen = QApplication.primaryScreen().geometry()
            self.resize(int(screen.width() * 0.75), int(screen.height() * 0.75))
            self.move(screen.center() - self.rect().center())
