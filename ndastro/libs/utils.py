"""Module to hold all the util defs."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, cast

from skyfield.api import load
from skyfield.data.spice import inertial_frames
from skyfield.elementslib import osculating_elements_of
from skyfield.framelib import ecliptic_frame
from skyfield.positionlib import Barycentric
from skyfield.toposlib import Topos
from skyfield.units import Angle, Distance

if TYPE_CHECKING:
    from skyfield.vectorlib import VectorSum

type PlanetName = str
type PlanetLatitude = Angle
type PlanetLongitude = Angle

type PlanetRADegrees = float
type PlanetDecDegrees = float

type PlanetPosition = tuple[PlanetName, PlanetLatitude, PlanetLongitude, Distance]
type SiderealPlanetPosition = tuple[PlanetName, PlanetDecDegrees, PlanetRADegrees, Distance]

eph = load("de440s.bsp")
ts = load.timescale()


def sign(num: int) -> int:
    """Return the sign of the given number.

    Args:
        num (int): number to get the sign from

    Returns:
        int: 1 with sign

    """
    return -1 if num < 0 else 1


def deg_to_dms(deg: float) -> tuple[int, int, int]:
    """Convert deg decimal to DegMinSec.

    Args:
        deg (float): The degree decimal

    Returns:
        DegMinSec: The instance of DegMinSec with deg values

    """
    m, s = divmod(abs(deg) * 3600, 60)
    d, m = divmod(m, 60)
    d = d * sign(int(d))

    return (int(d), int(m), int(s))


def get_ecliptic_position_of(planet_code: str, lat: Angle, lon: Angle, given_time: datetime) -> tuple[Angle, Angle, Distance]:
    """Return ecliptic position of the planet in the given lat, lon & datetime.

    Args:
        planet_code (str): One of planet code
        lat (Angle): Latitude of the observer
        lon (Angle): Longitude of the observer
        given_time (Time): Datetime of the observer

    Returns:
        tuple[Angle, Angle, Distance]: Ecliptic postion details about the planet

    """
    # Load ephemeris
    t = ts.utc(given_time)

    # Observer's location
    observer: VectorSum = eph["earth"] + Topos(latitude_degrees=lat.degrees, longitude_degrees=lon.degrees)
    astrometric = cast(Barycentric, observer.at(t)).observe(eph[planet_code]).apparent()

    return astrometric.frame_latlon(ecliptic_frame)


def get_tropical_position_of(planet_code: str, lat: Angle, lon: Angle, given_time: datetime) -> tuple[Angle, Angle, Distance]:
    """Return tropical position of the planet in the given lat, lon & datetime.

    Args:
        planet_code (str): One of planet code
        lat (Angle): Latitude of the observer
        lon (Angle): Longitude of the observer
        given_time (Time): Datetime of the observer

    Returns:
        tuple[Angle, Angle, Distance]: Postion details about the planet

    """
    t = ts.utc(given_time)

    # Observer's location
    # Define the observer location (for example, Bengaluru's latitude and longitude)
    observer: VectorSum = eph["earth"] + Topos(lat, lon)
    astrometric = cast(Barycentric, observer.at(t)).observe(eph[planet_code]).apparent()

    return astrometric.ecliptic_latlon()


def get_tropical_planetary_positions(lat: Angle, lon: Angle, given_time: datetime) -> list[PlanetPosition]:
    """Return tropical postions of the planets.

    Args:
        lat (Angle): Latitude of the observer i.e earth
        lon (Angle): Longitude of the observer
        given_time (Time): Datetime of the observer

    Returns:
        list[PlanetPosition]: List of planets

    """
    planets = {
        "Sun": "sun",
        "Moon": "moon",
        "Mercury": "mercury",
        "Venus": "venus",
        "Mars": "mars barycenter",
        "Jupiter": "jupiter barycenter",  # Use barycenter for outer planets
        "Saturn": "saturn barycenter",
        "Uranus": "uranus barycenter",
        "Neptune": "neptune barycenter",
        "Pluto": "pluto barycenter",
        "Rahu": "rahu",
        "Kethu": "kethu",
    }
    positions: list[PlanetPosition] = []

    for planet_name, planet_code in planets.items():
        if planet_code in ("rahu", "kethu"):
            nodes = calculate_lunar_nodes(given_time)
            positions.extend(nodes)
            continue

        lat, lon, distance = get_tropical_position_of(planet_code, lat, lon, given_time)

        positions.append(
            (
                planet_name,
                lat,
                lon,
                distance,
            ),
        )

    return positions


def calculate_lunar_nodes(given_time: datetime) -> list[PlanetPosition]:
    """Calculate lunar node's angle.

    Args:
        given_time (datetime): Datetime on which the node's position
        ayanamsa_value (float): Ayanamsa value

    Returns:
        dict[str, dict[str, float]]: Lunar position

    """
    t = ts.utc(given_time)
    ecliptic = inertial_frames["ECLIPJ2000"]

    earth = eph["earth"]
    moon = eph["moon"]
    position = (moon - earth).at(t)
    elements = osculating_elements_of(position, ecliptic)

    rahu_position = (cast(float, cast(Angle, elements.longitude_of_ascending_node).degrees)) % 360
    kethu_position = (rahu_position + 180) % 360

    # Placeholder values for declination and distance
    declination_placeholder = 0.0
    distance_placeholder = 0.00256955529  # Approx. average AU of Moon's distance

    return [
        (
            "rahu",
            Angle(degrees=declination_placeholder),
            Angle(degrees=rahu_position),
            Distance(au=distance_placeholder),
        ),
        (
            "kethu",
            Angle(degrees=declination_placeholder),
            Angle(degrees=kethu_position),
            Distance(au=distance_placeholder),
        ),
    ]
