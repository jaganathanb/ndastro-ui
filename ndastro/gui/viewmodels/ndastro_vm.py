"""Module to hold the view model."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from i18n import set as set_i18n_config
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication

if TYPE_CHECKING:
    from ndastro.core.settings.manager import SettingsManager

from ndastro.libs.utils import get_kattams

if TYPE_CHECKING:
    from ndastro.gui.models.kattam import Kattam
    from ndastro.gui.models.ndastro_model import NDAstroModel
    from ndastro.gui.ndastro import NDAstro

from qdarkstyle import DarkPalette, LightPalette, load_stylesheet


class NDAstroViewModel(QObject):
    """ViewModel to hold data & business.

    Args:
        QObject (_type_): _description_

    """

    language_changed = Signal(str)
    theme_changed = Signal(str)

    def __init__(self, model: NDAstroModel, settings_manager: SettingsManager) -> None:
        """Initialize the view model.

        Args:
            model (NDAstroModel): The model
            settings_manager (SettingsManager): The settings manager

        """
        super().__init__()
        self._model = model  # Reference to the model
        self._settings_manager = settings_manager
        self._get_kattams()

    @property
    def title(self) -> str:
        """Title of the main window.

        Returns:
            str: Title

        """
        return self._model.title

    @property
    def locales(self) -> list[tuple[str, str]]:
        """Return language supported.

        Returns:
            list[tuple[str, str]]: List of language name & key

        """
        return self._model.supported_language

    @locales.setter
    def locales(self, value: list[tuple[str, str]]) -> None:
        """Set the supported languages.

        Args:
            value (list[tuple[str, str]]): List of language name & key

        """
        self._model.supported_language = value

    @property
    def themes(self) -> list[tuple[str, str]]:
        """Return theme supported.

        Returns:
            list[tuple[str, str]]: List of theme name & key

        """
        return self._model.supported_theme

    @themes.setter
    def themes(self, value: list[tuple[str, str]]) -> None:
        """Set the supported themes.

        Args:
            value (list[tuple[str, str]]): List of theme name & key

        """
        self._model.supported_theme = value

    @property
    def kattams(self) -> list[Kattam] | None:
        """Return positions of the planets.

        Returns:
            list[PlanetDetail]: List of planet positions

        """
        return self._model.kattams

    @kattams.setter
    def kattams(self, value: list[Kattam]) -> None:
        """Set the positions of the planets.

        Args:
            value (list[PlanetDetail]): List of planet positions

        """
        self._model.kattams = value

    async def set_language(self, index: int) -> None:
        """Set language to be used.

        Args:
            index (int): _description_

        """
        lang = self.locales[index]
        set_i18n_config("locale", lang[1])

        await self._settings_manager.set_async("APP", "language", lang[1])
        self.language_changed.emit(lang[1])

    async def set_theme(self, index: int) -> None:
        """Set theme to be used.

        Args:
            index (int): _description_

        """
        theme = self.themes[index]

        app = QApplication.instance()
        if app is None:
            raise RuntimeError

        palette = DarkPalette if theme[1] == "dark" else LightPalette
        cast("NDAstro", app).setStyleSheet(load_stylesheet(qt_api="pyside6", palette=palette))

        await self._settings_manager.set_async("APP", "theme", theme[1])
        self.theme_changed.emit(theme[1])

    def _get_kattams(self) -> None:
        kattams = get_kattams(
            lat=self._model.latlon[0],
            lon=self._model.latlon[1],
            given_time=self._model.given_time,
        )

        self._model.set_kattams(kattams)
