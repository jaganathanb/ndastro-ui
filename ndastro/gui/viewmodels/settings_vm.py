"""Provide methods to manage application settings using a settings manager.

Includes functionality to load, save, and manipulate settings, as well as
convenience methods for retrieving specific types of settings.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ndastro.core.settings.manager import SettingsManager


class SettingsViewModel:
    """Manage application settings using a settings manager.

        Provide methods to load, save, and manipulate application settings.

    Attributes
    ----------
    settings_manager : SettingsManager
        The settings manager instance to manage application settings.
    settings : dict
        A dictionary to store the application settings.

    """

    def __init__(self, settings_manager: SettingsManager) -> None:
        """Initialize the SettingsViewModel with a settings manager.

        Parameters
        ----------
        settings_manager : SettingsManager
            The settings manager instance to manage application settings.

        """
        self.settings_manager = settings_manager
        self.settings = {}

    def load_settings(self) -> None:
        """Load all settings from the settings manager and store them in the settings dictionary."""
        self.settings = self.settings_manager.get_all()

    async def save_settings(self) -> None:
        """Save all current settings to the settings manager asynchronously."""
        await self.settings_manager.save_all(self.settings)

    def get(self, section: str, key: str, default: str | None = None) -> str | None:
        """Retrieve a setting value from the settings dictionary.

        Parameters
        ----------
        section : str
            The section of the settings to look in.
        key : str
            The key of the setting to retrieve.
        default : optional
            The default value to return if the key is not found.

        Returns
        -------
        str | None
            The value of the setting if found, otherwise the default value.

        """
        return self.settings.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: str) -> None:
        """Set a value in the settings dictionary.

        Parameters
        ----------
        section : str
            The section of the settings to modify.
        key : str
            The key of the setting to set.
        value : any
            The value to set for the specified key.

        """
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = str(value)

    # Convenience methods (optional)
    def get_bool(self, section: str, key: str, *, default: bool = False) -> bool:
        """Retrieve a boolean setting value from the settings dictionary.

        Parameters
        ----------
        section : str
            The section of the settings to look in.
        key : str
            The key of the setting to retrieve.
        default : bool, optional
            The default value to return if the key is not found, False by default.

        Returns
        -------
        bool
            The boolean value of the setting if found, otherwise the default value.

        """
        val = str(self.get(section, key, str(default))).lower()
        return val in ["true", "1", "yes", "on"]

    def get_int(self, section: str, key: str, default: int = 0) -> int:
        """Retrieve an integer setting value from the settings dictionary.

        Parameters
        ----------
        section : str
            The section of the settings to look in.
        key : str
            The key of the setting to retrieve.
        default : int, optional
            The default value to return if the key is not found, 0 by default.

        Returns
        -------
        int
            The integer value of the setting if found and valid, otherwise the default value.

        """
        try:
            value = self.get(section, key, str(default))
            return int(value) if value is not None else default
        except ValueError:
            return default
