"""Module to hold planet postion related data classes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skyfield.units import Angle

    from ndastro.gui.models.planet_position import PlanetDetail
    from ndastro.libs.house_enum import Houses
    from ndastro.libs.planet_enum import Planets
    from ndastro.libs.rasi_enum import Rasis


@dataclass
class Kattam:
    """Holds data for each square (kattam/கட்டம்) on the chart."""

    order: int
    is_ascendant: bool
    asc_longitude: Angle | None
    owner: Planets
    rasi: Rasis
    house: Houses
    planets: list[PlanetDetail] | None
