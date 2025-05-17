"""Define the SettingsDialog class for managing application settings.

The SettingsDialog provides a user interface for modifying and saving
application settings, including general and appearance settings.
"""

import asyncio

from PySide6.QtCore import Signal, SignalInstance
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
)

from ndastro.gui.viewmodels.settings_vm import SettingsViewModel
from ndastro.gui.views.controls.dialogs.base_dialog_content import (
    BaseDialogContent,
)
from ndastro.gui.views.widgets.setting_sections.appearance_section import (
    AppearanceSection,
)
from ndastro.gui.views.widgets.setting_sections.genenral_section import (
    GeneralSection,
)


class SettingsDialog(BaseDialogContent):
    """A dialog for managing application settings.

    This dialog provides a user interface for modifying and saving
    application settings, including general and appearance settings.

    Attributes:
        view_model (NDAstroViewModel): The view model for managing application settings.
        sidebar (QListWidget): The sidebar for selecting settings sections.
        stack (QStackedWidget): The stacked widget for displaying settings sections.
        save_button (QPushButton): The button to save settings.
        reset_button (QPushButton): The button to reset settings to defaults.
        close_button (QPushButton): The button to close the dialog.

    """

    _close_dialog = Signal(str)

    def __init__(self, view_model: SettingsViewModel) -> None:
        """Initialize the settings dialog.

        Args:
            view_model (SettingsViewModel): The view model for managing application settings.

        """
        super().__init__()

        self.view_model = view_model
        self.setWindowTitle("Application Settings")

        self.sidebar = QListWidget()
        self.stack = QStackedWidget()
        self.save_button = QPushButton("Save")
        self.reset_button = QPushButton("Reset")
        self.close_button = QPushButton("Close")

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        self.sidebar.addItem(QListWidgetItem("General"))
        self.sidebar.addItem(QListWidgetItem("Appearance"))

        self.stack.addWidget(GeneralSection(self.view_model))
        self.stack.addWidget(AppearanceSection(self.view_model))

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack, 1)

        layout = QVBoxLayout(self)
        layout.addLayout(main_layout)
        layout.addLayout(button_layout)

    def _connect_signals(self) -> None:
        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.save_button.clicked.connect(lambda: asyncio.create_task(self._save_and_close()))
        self.reset_button.clicked.connect(self.view_model.load_settings)
        self.close_button.clicked.connect(lambda: self._close_dialog.emit("close"))

    async def _save_and_close(self) -> None:
        await self.view_model.save_settings()
        self._close_dialog.emit()

    def show_event(self, arg__1: QShowEvent) -> None:
        """Override show_event to load settings when the dialog is shown."""
        self.view_model.load_settings()
        super().showEvent(arg__1)

    @property
    def close_dialog(self) -> SignalInstance:
        """Signal emitted to request closing the dialog."""
        return self._close_dialog
