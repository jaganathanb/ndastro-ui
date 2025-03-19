"""Module to hold the ndastro model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from i18n import t

if TYPE_CHECKING:
    from datetime import datetime

    from skyfield.units import Angle

    from ndastro.gui.models.planet_position import PlanetDetail


class NDAstroModel:
    """Model for the NDAstro."""

    def __init__(
        self,
        given_time: datetime,
        latlon: tuple[Angle, Angle],
        locales: list[tuple[str, str]],
    ) -> None:
        """Initialize the model."""
        self.title = t("common.appTitle")
        self.given_time = given_time
        self.latlon = latlon
        self.supported_language: list[tuple[str, str]] = locales
        self.planet_positions: list[PlanetDetail] | None = []

    def set_planet_positions(self, positions: list[PlanetDetail]) -> None:
        """Set the planet positions.

        Args:
            positions (list[PlanetDetail]): List of planet positions

        """
        self.planet_positions = positions
