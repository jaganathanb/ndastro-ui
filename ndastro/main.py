"""Module providing a function printing python version."""

import sys
from pathlib import Path
from signal import SIGINT, signal

import py_hot_reload
from i18n import set as set_i18n_config
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication

from ndastro.gui.models.ndastro_model import NDAstroModel
from ndastro.gui.viewmodels.ndastro_viewmodel import NDAstroViewModel
from ndastro.gui.views.ndastro_ui import NDAstroMainWindow

basedir = Path(__file__).resolve().parent


def _configure_i18n(basedir: Path) -> None:
    set_i18n_config("file_format", "json")
    set_i18n_config("filename_format", "{namespace}.{locale}.{format}")
    set_i18n_config("load_path", [Path.joinpath(basedir, "locales")])
    set_i18n_config("skip_locale_root_data", value=True)


def init() -> None:
    """Initilize the app."""
    app = QApplication(sys.argv)
    pix = QPixmap(Path.joinpath(basedir, "icons", "hand.ico"))
    app.setWindowIcon(QIcon(pix))

    _configure_i18n(basedir)

    model = NDAstroModel([("English", "en"), ("Tamil", "ta")])
    view_model = NDAstroViewModel(model)

    w = NDAstroMainWindow(view_model)
    w.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    signal(SIGINT, lambda _, __: QApplication.quit())
    init()


def reload() -> None:
    app = QApplication.instance()
    if app is not None:
        app.quit()
    init()


py_hot_reload.run_with_reloader(reload)
