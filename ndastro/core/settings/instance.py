"""Initialize the settings manager.

Provide a single instance of SettingsManager for managing application settings.
"""

from .manager import SettingsManager

# Create single instance when module is imported
settings_manager = SettingsManager()

__all__ = ["settings_manager"]
