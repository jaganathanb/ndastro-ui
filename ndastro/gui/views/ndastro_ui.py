"""ND Astro module."""

from i18n.translator import t
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ndastro.gui.viewmodels.ndastro_viewmodel import NDAstroViewModel
from ndastro.libs.south_chart import ResizableAstroChart


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

        # Split window into top bottom part
        self.h_layout = QHBoxLayout()
        self.setLayout(self.h_layout)

        self.vl_left_frame = QVBoxLayout()

        self.left_frame = QFrame()
        self.h_layout.addWidget(self.left_frame)

        self.h_layout.setStretchFactor(self.left_frame, 10)

        self.left_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_frame.setLayout(self.vl_left_frame)

        self.vl_left_frame.addWidget(ResizableAstroChart(), 0)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        self._create_language_selector()

        toolbar.addWidget(self.combo)

        self._create_actions()
        self._create_menus()

        container = QWidget()
        container.setLayout(self.h_layout)

        self.setCentralWidget(container)

        self.show()

    def _create_language_selector(self) -> None:
        """Create language selector."""
        self.combo = QComboBox()
        options = self._view_model.locales
        for _, (text, _) in enumerate(options):
            self.combo.addItem(text)

        self.combo.currentIndexChanged.connect(self._view_model.set_language)

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
