"""ND Astro module."""

from i18n.translator import t
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ndastro.gui.viewmodels.ndastro_viewmodel import NDAstroViewModel


class NDAstroMainWindow(QMainWindow):
    """Module providing a function printing python version."""

    def __init__(self, view_model: NDAstroViewModel) -> None:
        """Initialize the app."""
        super().__init__()
        self._view_model = view_model

        self._view_model.language_changed.connect(self._set_language)

        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI."""
        self.setWindowTitle(self._view_model.title)
        self.vb_layout = QVBoxLayout()
        self.vb_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._create_language_selector()
        self._create_actions()
        self._create_menus()

        container = QWidget()
        container.setLayout(self.vb_layout)

        self.setCentralWidget(container)

        self.show()

    def _create_language_selector(self) -> None:
        """Create language selector."""
        self.combo = QComboBox()
        options = self._view_model.locales
        for _, (text, _) in enumerate(options):
            self.combo.addItem(text)

        self.combo.currentIndexChanged.connect(self._view_model.set_language)

        hb_layout = QHBoxLayout()
        hb_layout.addWidget(self.combo, 0, Qt.AlignmentFlag.AlignRight)
        self.vb_layout.addLayout(hb_layout)

    def _set_language(self) -> None:
        self._retranslate_ui()

    def _retranslate_ui(self) -> None:
        self.setWindowTitle(t("common.appTitle"))

    def _create_actions(self) -> None:
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+X")
        self.exit_action.triggered.connect(self.close)

        self.about_action = QAction("About", self)
        self.about_action.setShortcut("F1")
        self.about_action.triggered.connect(self._about)

    def _create_menus(self) -> None:
        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.exit_action)

        self.options_menu = self.menuBar().addMenu("Options")

        self.menuBar().addSeparator()

        self.help_menu = self.menuBar().addMenu("Help")
        self.help_menu.addAction(self.about_action)

    @Slot()
    def _about(self) -> None:
        QMessageBox.about(
            self,
            "About Settings Editor",
            "The <b>Settings Editor</b> example shows how to access application settings using Qt.",
        )
