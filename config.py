"""Configuration module for the application.

This module defines constants and default settings used throughout the application,
such as application paths, database configuration, and default user settings.
"""

from pathlib import Path

import darkdetect

# Application paths
APP_NAME = "ND Astro"
APP_AUTHOR = "Jaganathan Bantheswaran"

# Database configuration
DATA_DIR = Path.home() / f".{APP_NAME.lower().replace(' ', '_')}"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = str(DATA_DIR / "settings.db")

# Settings defaults
DEFAULT_SETTINGS = {
    "theme": "dark" if darkdetect.isDark() else "light",
    "language": "en",
    "timezone": "Asia/Kolkata",
    "date_format": "%d-%m-%Y",
    "time_format": "%H:%M:%S",
    "recent_files": [],
}
