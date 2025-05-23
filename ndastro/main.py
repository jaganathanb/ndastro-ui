"""Module providing a function printing python version."""

import logging
import sys
from datetime import datetime
from pathlib import Path

import pytz
from dependency_injector.wiring import Provide, inject
from i18n import set as set_i18n_config
from PySide6 import QtAsyncio
from PySide6.QtCore import QFile, QTextStream
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication
from qdarkstyle import DarkPalette, LightPalette, load_stylesheet
from skyfield.units import Angle

from ndastro.app_container import AppContainer
from ndastro.core.settings.manager import SettingsManager
from ndastro.gui.models.ndastro_model import NDAstroModel
from ndastro.gui.ndastro import NDAstro
from ndastro.gui.views.ndastro_ui import NDAstroMainWindow
from resources import *  # noqa: F403


def _configure_i18n(basedir: Path, lang: str) -> None:
    set_i18n_config("file_format", "json")
    set_i18n_config("filename_format", "{namespace}.{locale}.{format}")
    set_i18n_config("load_path", [Path.joinpath(basedir, "resources", "locales")])
    set_i18n_config("skip_locale_root_data", value=True)
    set_i18n_config("locale", lang)


def init(app: QApplication, settings_manager: SettingsManager, ndastro_view: NDAstroMainWindow, logger: logging.Logger) -> None:
    """Initilize the app."""
    app.setApplicationName(settings_manager.get("APP", "app_name"))
    app.setApplicationVersion(settings_manager.get("APP", "app_version"))

    pix = QPixmap(str(Path(settings_manager.get("APP", "app_icon")).resolve()))
    app.setWindowIcon(QIcon(pix))

    file = QFile(":/styles/core.qss")
    file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    stream = QTextStream(file)
    stylesheet = stream.readAll()
    file.close()

    palette = DarkPalette if settings_manager.get("APP", "theme") == "dark" else LightPalette
    app.setStyleSheet(load_stylesheet(qt_api="pyside6", palette=palette) + stylesheet)

    ndastro_view.show()
    logger.info("NDAstro view displayed.")

    QtAsyncio.run(handle_sigint=True)


@inject
def start(
    app: QApplication,
    settings_manager: SettingsManager = Provide[AppContainer.core_package.container.settings_manager],
    ndastro_view: NDAstroMainWindow = Provide[AppContainer.gui_package.container.ndastro_view],
) -> None:
    """Entry point for the application.

    This function initializes the application by calling the init() function.
    """
    logger = logging.getLogger(__name__)
    init(app, settings_manager, ndastro_view, logger)


def main() -> None:
    """Set up and start the NDAstro application.

    This function sets up the application container, initializes resources,
    configures internationalization, and starts the NDAstro application.
    """
    base_dir = Path(__file__).resolve().parent

    container = AppContainer()
    container.core_package.init_resources()
    container.wire(modules=[__name__])

    settings_manager = container.core_package.container.settings_manager()

    _configure_i18n(base_dir, settings_manager.get("APP", "language"))

    latlong = settings_manager.get("APP", "location").split(",")
    lat, lon = [float(coord) for coord in latlong]

    container.gui_package.container.ndastro_model.override(
        NDAstroModel(
            datetime.now(pytz.timezone(settings_manager.get("APP", "timezone"))),
            (Angle(degrees=lat), Angle(degrees=lon)),
            [("English", "en"), ("Tamil", "ta")],
            [("Light", "light"), ("Dark", "dark")],
        ),
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting the NDAstro application...")

    app = NDAstro([*sys.argv])
    start(app)
    logger.info("NDAstro application finished.")

    container.core_package.container.shutdown_resources()
    logger.info("NDAstro application resources cleaned up.")


if __name__ == "__main__":
    main()
