"""Module to hold the view model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from i18n import set as set_i18n_config
from PySide6.QtCore import QObject, Signal

from ndastro.libs.utils import get_tropical_planetary_positions

if TYPE_CHECKING:
    from ndastro.gui.models.ndastro_model import NDAstroModel
    from ndastro.gui.models.planet_position import PlanetPosition


class NDAstroViewModel(QObject):
    """ViewModel to hold data & business.

    Args:
        QObject (_type_): _description_

    """

    language_changed = Signal(str)

    def __init__(self, model: NDAstroModel) -> None:
        """Initialize the view model.

        Args:
            model (NDAstroModel): The model

        """
        super().__init__()
        self._model = model  # Reference to the model
        self._get_planet_positions()

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

    @property
    def planet_positions(self) -> list[PlanetPosition] | None:
        """Return positions of the planets.

        Returns:
            list[PlanetPosition]: List of planet positions

        """
        return self._model.planet_positions

    def set_language(self, index: int) -> None:
        """Set language to be used.

        Args:
            index (int): _description_

        """
        lang = self.locales[index]
        set_i18n_config("locale", lang[1])
        self.language_changed.emit(lang[1])

    def _get_planet_positions(self) -> None:
        positions = get_tropical_planetary_positions(
            lat=self._model.latlon[0],
            lon=self._model.latlon[1],
            given_time=self._model.given_time,
        )

        self._model.set_planet_positions(positions)
