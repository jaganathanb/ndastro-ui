"""Settings Manager Module.

This module provides functionality to manage application settings using a configuration file.
It includes a notifier for signaling changes and ensures thread-safe operations.
"""

import configparser
import logging
from pathlib import Path

from PySide6.QtCore import QMutex, QMutexLocker, QObject, Signal

logger = logging.getLogger(__name__)


class SettingsNotifier(QObject):
    """A notifier class to signal when a setting has changed.

    Attributes
    ----------
    setting_changed : Signal
        A signal emitted when a setting changes, providing the key and new value.

    """

    setting_changed = Signal(str, str, str)  # section, key, value


class SettingsManager:
    """Manages application settings using a configuration file.

    This class provides methods to load, retrieve, update, and save settings
    in a thread-safe manner. It also notifies listeners when a setting changes.
    """

    def __init__(self, config_file: str = "settings.ini") -> None:
        """Initialize the SettingsManager with a configuration file.

        Parameters
        ----------
        config_file : str, optional
            The name of the configuration file to load, defaults to "settings.ini".

        """
        self.notifier = SettingsNotifier()
        self._listener_thread = None
        self._last_change_id = 0
        self._mutex = QMutex()  # Mutex for thread safety

        self._config_file = config_file
        self.config_parser = self._load(config_file)

    def _load(self, config_file: str) -> configparser.ConfigParser:
        """Load the application settings from the configuration file.

        This method ensures that the base INI file exists in the user's home directory
        under the `.ndastro` folder. If the file does not exist, it creates the file.
        It initializes a `ConfigParser` instance, reads the configuration from the file,
        and sets default application settings if they are not already present.

        Returns:
            configparser.ConfigParser: An instance of `ConfigParser` containing the
            loaded settings.

        Raises:
            OSError: If there is an issue creating the base INI file or accessing the
            directory.

        Notes:
            - The default settings include application language, theme, locale, timezone,
              date and time formats, geometric settings, location, location name, and
              recent files.
            - The method uses a thread-safe mechanism (`QMutexLocker`) to ensure that
              the configuration file is accessed safely in a multi-threaded environment.

        """
        with QMutexLocker(self._mutex):
            logger.info("Inside create_instance")
            data_dir = Path.home() / ".ndastro"
            data_dir.mkdir(exist_ok=True)
            base_ini_file = data_dir / config_file

            if not base_ini_file.exists():
                Path.touch(base_ini_file)
                logger.info("The base INI file was NOT found in this directory, so created it.", extra={"file_path": base_ini_file})
            else:
                logger.info("The base INI file was found in this directory.", extra={"file_path": base_ini_file})
            self._config_file = base_ini_file

            # Initialize the ConfigParser instance
            config_parser = configparser.ConfigParser()

            config_parser.read(base_ini_file)
            config_parser.setdefault(
                "APP",
                {
                    "app_name": "ND Astro",
                    "app_version": "0.1.0",
                    "app_description": "A simple astronomy application.",
                    "app_icon_path": str(Path(__file__).parent.parent.parent / "resources" / "icons" / "ndastro.png"),
                    "app_author": "Jaganathan B",
                    "app_author_email": "Jaganathan[dot]Eswaran[at]gmail[dot]com",
                    "recent_files_limit": "5",
                    "recent_files": "",
                    "language": "en",
                    "theme": "light",
                    "locale": "en_US",
                    "timezone": "Asia/Kolkata",
                    "date_format": "%%Y-%%m-%%d",
                    "time_format": "%%H:%%M:%%S",
                    "geometrics": "0,0,0,0",
                    "location": "12.9716,77.5946",
                    "location_name": "Bangalore",
                },
            )
            return config_parser

    def get(self, section: str, key: str, fallback: str = "") -> str:
        """Retrieve a configuration value for a given section and key.

        Parameters
        ----------
        section : str
            The section in the configuration file.
        key : str
            The key within the section to retrieve the value for.
        fallback : str, optional
            The default value to return if the key is not found, defaults to an empty string.

        Returns
        -------
        str
            The value associated with the given key in the specified section, or the fallback value.

        """
        with QMutexLocker(self._mutex):
            return self.config_parser.get(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: object = None) -> None:
        """Set a configuration value for a given section and key.

        Parameters
        ----------
        section : str
            The section in the configuration file.
        key : str
            The key within the section to set the value for.
        value : object, optional
            The value to set for the given key, defaults to an None.

        """
        with QMutexLocker(self._mutex):
            if section not in self.config_parser:
                self.config_parser[section] = {}
            old_value = self.config_parser[section].get(key)
            self.config_parser[section][key] = str(value)
            self.save()
            if old_value != str(value):
                self.notifier.setting_changed.emit(section, key, str(value))

    def save(self) -> None:
        """Save the current configuration to the configuration file.

        This method writes the current state of the `ConfigParser` instance
        to the configuration file in a thread-safe manner.
        """
        with QMutexLocker(self._mutex), Path(self._config_file).open("w") as configfile:
            self.config_parser.write(configfile)
            logger.info("Configuration saved to %s", self._config_file)
