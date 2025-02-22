"""Module to hold planet postion related data classes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ndastro.libs.planet_enum import Planets
from ndastro.libs.rasi_enum import Rasis

if TYPE_CHECKING:
    from skyfield.units import Angle, Distance

    from ndastro.libs.house_enum import Houses


@dataclass
class PlanetPosition:
    """Represents the position of a planet with various attributes.

    Attributes:
        name (str): The name of the planet.
        latitude (Angle): The latitude of the planet's position.
        longitude (Angle): The longitude of the planet's position.
        distance (Distance): The distance of the planet from a reference point.
        s_longitude (Angle | None): The sidereal longitude of the planet, if applicable.
        posited_at (Houses | None): The house in which the planet is posited, if applicable.
        advanced_by (Angle | None): The angle by which the planet has advanced, if applicable.
        retrograde (bool): Indicates whether the planet is in retrograde motion.
        rasi_occupied (Rasis | None): The rasi (zodiac sign) occupied by the planet, if applicable.
        is_ascendant (bool): Indicates whether the planet is the ascendant.
        planet (Planets): The planet associated with this position.

    """

    name: str
    """The name of the planet."""

    latitude: Angle
    """The latitude of the planet's position."""

    longitude: Angle
    """The longitude of the planet's position."""

    planet: Planets = Planets.EMPTY
    """The planet associated with this position."""

    distance: Distance | None = None
    """The distance of the planet from a reference point."""

    s_longitude: Angle | None = None
    """The sidereal longitude of the planet, if applicable."""

    posited_at: Houses | None = None
    """The house in which the planet is posited, if applicable."""

    advanced_by: Angle | None = None
    """The angle by which the planet has advanced, if applicable."""

    retrograde: bool = False
    """Indicates whether the planet is in retrograde motion."""

    rasi_occupied: Rasis | None = None
    """The rasi (zodiac sign) occupied by the planet, if applicable."""

    is_ascendant: bool = False
    """Indicates whether the planet is the ascendant."""
