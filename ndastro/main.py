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
from skyfield.units import Angle

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

    pix = QPixmap(":/icons/hand.png")
    app.setWindowIcon(QIcon(pix))

    base_dir = Path(__file__).resolve().parent
    _configure_i18n(base_dir)

    model = NDAstroModel(
        datetime.now(pytz.timezone("Asia/Kolkata")),
        (Angle(degrees=12.38), Angle(degrees=77.54)),
        [("English", "en"), ("Tamil", "ta")],
        [("Light", "light"), ("Dark", "dark")],
    )
    view_model = NDAstroViewModel(model)

    w = NDAstroMainWindow(view_model)
    w.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    signal(SIGINT, lambda _, __: QApplication.quit())
    init()


def main() -> None:
    """Entry point for the application.

    This function initializes the application by calling the init() function.
    """
    init()
