"""Define the SettingsWindow class, which provides a GUI for managing application settings.

Display the current theme and update the UI when settings change.
"""

from typing import cast

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ndastro.core.settings.manager import SettingsManager


class SettingsWindow(QWidget):
    """A window for managing application settings.

    This class provides a GUI to display and update application settings,
    such as the current theme, and listens for changes to update the UI dynamically.
    """

    def __init__(self, settings_manager: SettingsManager) -> None:
        """Initialize the SettingsWindow with a settings manager.

        Args:
            settings_manager: An object that manages application settings.

        """
        super().__init__()
        self.settings = settings_manager

        # Setup UI
        self.label = QLabel("Current Theme: " + cast("str", self.settings.get("theme", "light")))
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Connect to changes
        self.settings.notifier.setting_changed.connect(self.on_setting_changed)
        self.settings.start_change_listener()

    def on_setting_changed(self, key: str, value: object) -> None:
        """Handle changes to application settings.

        Updates the UI when a setting is changed.

        Args:
            key (str): The name of the setting that changed.
            value (object): The new value of the setting.

        """
        if key == "theme":
            self.label.setText(f"Current Theme: {value}")
