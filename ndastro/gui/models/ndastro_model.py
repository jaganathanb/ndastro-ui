"""Module to hold the ndastro model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from i18n import t

from ndastro.core.settings.manager import SettingsManager
from ndastro.gui.models.kattam import Kattam

if TYPE_CHECKING:
    from datetime import datetime

    from skyfield.units import Angle

    from ndastro.gui.models.kattam import Kattam


class NDAstroModel:
    """Model for the NDAstro."""

    def __init__(
        self,
        given_time: datetime,
        latlon: tuple[Angle, Angle],
        locales: list[tuple[str, str]],
        themes: list[tuple[str, str]],
        settings: SettingsManager,
    ) -> None:
        """Initialize the model."""
        self.title = t("common.appTitle")
        self.settings = settings
        self.given_time = given_time
        self.latlon = latlon
        self.supported_theme: list[tuple[str, str]] = themes
        self.supported_language: list[tuple[str, str]] = locales
        self.kattams: list[Kattam] | None = []

    def set_kattams(self, kattams: list[Kattam]) -> None:
        """Set the kattams.

        Args:
            kattams (list[Kattam]): List of kattams

        """
        self.kattams = kattams
