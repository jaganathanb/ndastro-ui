"""Module providing a function printing python version."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from signal import SIGINT, signal

import pytz
from i18n import set as set_i18n_config
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication
from qdarkstyle import DarkPalette, LightPalette, load_stylesheet
from skyfield.units import Angle

from config import DEFAULT_SETTINGS
from ndastro.core.database.models import SettingsModel
from ndastro.core.settings.instance import settings_manager
from ndastro.gui.models.ndastro_model import NDAstroModel
from ndastro.gui.ndastro import NDAstro
from ndastro.gui.viewmodels.ndastro_viewmodel import NDAstroViewModel
from ndastro.gui.views.ndastro_ui import NDAstroMainWindow
from resources import *  # noqa: F403

basedir = Path(__file__).resolve().parent


def _configure_i18n(basedir: Path) -> None:
    set_i18n_config("file_format", "json")
    set_i18n_config("filename_format", "{namespace}.{locale}.{format}")
    set_i18n_config("load_path", [Path.joinpath(basedir, "resources", "locales")])
    set_i18n_config("skip_locale_root_data", value=True)


def init() -> None:
    """Initilize the app."""
    app = NDAstro([*sys.argv])

    logging.basicConfig(level=logging.DEBUG)

    pix = QPixmap(str(Path(basedir, "resources", "icons", "ndastro.png")))
    app.setWindowIcon(QIcon(pix))

    base_dir = Path(__file__).resolve().parent
    _configure_i18n(base_dir)

    initialize_application()

    palette = DarkPalette if settings_manager.get("theme") == "dark" else LightPalette
    app.setStyleSheet(load_stylesheet(qt_api="pyside6", palette=palette))

    model = NDAstroModel(
        datetime.now(pytz.timezone("Asia/Kolkata")),
        (Angle(degrees=12.38), Angle(degrees=77.54)),
        [("English", "en"), ("Tamil", "ta")],
        [("Light", "light"), ("Dark", "dark")],
        settings_manager,
    )
    view_model = NDAstroViewModel(model)

    w = NDAstroMainWindow(view_model)
    w.showMaximized()

    ret = app.exec()

    # Cleanup
    settings_manager.stop_change_listener()
    from core.database.connection import DatabaseConnection

    DatabaseConnection.close_all()

    sys.exit(ret)


def initialize_application() -> None:
    """Initialize the application.

    This function sets up the database schema, starts the settings change listener,
    and ensures default settings are applied if they do not exist.
    """
    # Initialize database
    SettingsModel.initialize_schema()

    # Initialize settings
    settings_manager.start_change_listener()

    # Set default settings if they don't exist
    if settings_manager.get("theme") is None:
        settings_manager.set("theme", DEFAULT_SETTINGS["theme"])
    if settings_manager.get("language") is None:
        settings_manager.set("language", DEFAULT_SETTINGS["language"])
    if settings_manager.get("timezone") is None:
        settings_manager.set("timezone", DEFAULT_SETTINGS["timezone"])
    if settings_manager.get("date_format") is None:
        settings_manager.set("date_format", DEFAULT_SETTINGS["date_format"])
    if settings_manager.get("time_format") is None:
        settings_manager.set("time_format", DEFAULT_SETTINGS["time_format"])
    if settings_manager.get("recent_files") is None:
        settings_manager.set("recent_files", DEFAULT_SETTINGS["recent_files"])


if __name__ == "__main__":
    signal(SIGINT, lambda _, __: QApplication.quit())
    init()


def main() -> None:
    """Entry point for the application.

    This function initializes the application by calling the init() function.
    """
    init()
