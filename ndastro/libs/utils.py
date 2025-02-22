"""Module to hold all the util defs."""

from __future__ import annotations

from datetime import datetime
from math import atan2, cos, degrees, radians, sin, tan
from typing import TYPE_CHECKING, cast

from ndastro.gui.models.planet_position import PlanetPosition

if TYPE_CHECKING:
    from ndastro.gui.models.kattam import Kattam

from skyfield.api import load
from skyfield.data.spice import inertial_frames
from skyfield.elementslib import osculating_elements_of
from skyfield.framelib import ecliptic_frame
from skyfield.nutationlib import mean_obliquity
from skyfield.positionlib import Barycentric
from skyfield.toposlib import Topos
from skyfield.units import Angle, Distance
from skyfield.vectorlib import VectorSum

from ndastro.libs.ayanamsa import get_lahiri_ayanamsa
from ndastro.libs.constants import AYANAMSA, DEGREE_MAX
from ndastro.libs.house_enum import Houses
from ndastro.libs.rasi_enum import Rasis

if TYPE_CHECKING:
    from ndastro.gui.models.kattam import Kattam

eph = load("de440s.bsp")
ts = load.timescale()


def sign(num: int) -> int:
    """Return the sign of the given number.

    Args:
        num (int): The number to get the sign from.

    Returns:
        int: -1 if the number is negative, otherwise 1.

    """
    return -1 if num < 0 else 1


def deg_to_dms(deg: float) -> tuple[int, int, int]:
    """Convert degrees in decimal format to degrees, minutes, and seconds.

    Args:
        deg (float): The degree in decimal format.

    Returns:
        tuple[int, int, int]: The degrees, minutes, and seconds.

    """
    m, s = divmod(abs(deg) * 3600, 60)
    d, m = divmod(m, 60)
    d = d * sign(int(d))

    return (int(d), int(m), int(s))


def get_ecliptic_position_of(planet_code: str, lat: Angle, lon: Angle, given_time: datetime) -> tuple[Angle, Angle, Distance]:
    """Return the ecliptic position of the planet for the given latitude, longitude, and datetime.

    Args:
        planet_code (str): The code of the planet.
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        given_time (datetime): The datetime of the observation.

    Returns:
        tuple[Angle, Angle, Distance]: The ecliptic latitude, longitude, and distance of the planet.

    """
    t = ts.utc(given_time)
    observer: VectorSum = eph["earth"] + Topos(latitude_degrees=lat.degrees, longitude_degrees=lon.degrees)
    astrometric = cast(Barycentric, observer.at(t)).observe(eph[planet_code]).apparent()

    return astrometric.frame_latlon(ecliptic_frame)


def get_tropical_position_of(planet_code: str, lat: Angle, lon: Angle, given_time: datetime) -> tuple[Angle, Angle, Distance]:
    """Return the tropical position of the planet for the given latitude, longitude, and datetime.

    Args:
        planet_code (str): The code of the planet.
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        given_time (datetime): The datetime of the observation.

    Returns:
        tuple[Angle, Angle, Distance]: The tropical latitude, longitude, and distance of the planet.

    """
    t = ts.utc(given_time)
    observer: VectorSum = eph["earth"] + Topos(lat, lon)
    astrometric = cast(Barycentric, observer.at(t)).observe(eph[planet_code]).apparent()

    return astrometric.ecliptic_latlon()


def get_tropical_planetary_positions(lat: Angle, lon: Angle, given_time: datetime) -> list[PlanetPosition]:
    """Return the tropical positions of the planets.

    Args:
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        given_time (datetime): The datetime of the observation.

    Returns:
        list[PlanetPosition]: A list of tropical positions of the planets.

    """
    planets = {
        "Sun": "sun",
        "Moon": "moon",
        "Mercury": "mercury",
        "Venus": "venus",
        "Mars": "mars barycenter",
        "Jupiter": "jupiter barycenter",
        "Saturn": "saturn barycenter",
        "Rahu": "rahu",
    }
    positions: list[PlanetPosition] = []

    for planet_name, planet_code in planets.items():
        if planet_code == "rahu":
            nodes = calculate_lunar_nodes(given_time)
            positions.extend(nodes)
            continue

        lat, lon, distance = get_tropical_position_of(planet_code, lat, lon, given_time)

        positions.append(
            PlanetPosition(
                planet_name,
                lat,
                lon,
            ),
        )

    return positions


def calculate_lunar_nodes(given_time: datetime) -> list[PlanetPosition]:
    """Calculate the positions of the lunar nodes.

    Args:
        given_time (datetime): The datetime of the observation.

    Returns:
        list[PlanetPosition]: A list containing the positions of Rahu and Kethu.

    """
    t = ts.utc(given_time)
    ecliptic = inertial_frames["ECLIPJ2000"]

    earth = eph["earth"]
    moon = eph["moon"]
    position = cast(VectorSum, (moon - earth)).at(t)
    elements = osculating_elements_of(position, ecliptic)

    rahu_position = (cast(float, cast(Angle, elements.longitude_of_ascending_node).degrees)) % 360
    kethu_position = (rahu_position + 180) % 360

    declination_placeholder = 0.0

    return [
        PlanetPosition(
            "rahu",
            Angle(degrees=declination_placeholder),
            Angle(degrees=rahu_position),
        ),
        PlanetPosition(
            "kethu",
            Angle(degrees=declination_placeholder),
            Angle(degrees=kethu_position),
        ),
    ]


def get_sidereal_planet_positions(lat: Angle, lon: Angle, given_time: datetime, ayanamsa: float) -> list[PlanetPosition]:
    """Return the sidereal positions of the planets.

    Args:
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        given_time (datetime): The datetime of the observation.
        ayanamsa (float): The ayanamsa value to be used for calculation.

    Returns:
        list[PlanetPosition]: A list of sidereal positions of the planets.

    """
    positions = get_tropical_planetary_positions(lat, lon, given_time)
    asc_pos = get_sidereal_ascendant_position(given_time, lat, lon, ayanamsa)

    for pos in positions:
        asc = normalize_degree(cast(float, pos.longitude.degrees) - ayanamsa)

        asc_h, asc_adv_by = divmod(asc, 30)
        rasi_num = normalize_rasi(int(asc_h))

        pos.s_longitude = Angle(degrees=asc)
        pos.rasi_occupied = Rasis(rasi_num if asc_adv_by == 0 else int(rasi_num + 1))
        pos.posited_at = cast(Houses, cast(Houses, asc_pos.posited_at) + Houses(rasi_num if asc_adv_by == 0 else int(rasi_num + 1)))
        pos.advanced_by = Angle(degrees=asc_adv_by)

    positions.append(asc_pos)

    return positions


def get_tropical_ascendant_position(given_time: datetime, lat: Angle, lon: Angle) -> Angle:
    """Calculate the tropical ascendant.

    Args:
        given_time (datetime): The datetime of the observation.
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.

    Returns:
        Angle: The longitude of the tropical ascendant.

    """
    ts = load.timescale()
    t = ts.utc(given_time)

    oe = mean_obliquity(t.tdb) / 3600
    oer = radians(oe)

    gmst: float = cast(float, t.gmst)

    lst = (gmst + cast(float, lon.degrees) / 15) % 24

    lstr = radians(lst * 15)

    ascr = atan2(cos(lstr), -(sin(lstr) * cos(oer) + tan(radians(cast(float, lat.degrees))) * sin(oer)))

    asc = degrees(ascr)

    return Angle(degrees=asc)


def get_sidereal_ascendant_position(given_time: datetime, lat: Angle, lon: Angle, ayanamsa: float = AYANAMSA.LAHIRI) -> PlanetPosition:
    """Calculate the sidereal ascendant.

    Args:
        given_time (datetime): The datetime of the observation.
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        ayanamsa (float): The ayanamsa value to be used for calculation.

    Returns:
        PlanetPosition: The position of the sidereal ascendant.

    """
    ascr = get_tropical_ascendant_position(given_time, lat, lon)

    asc = normalize_degree(cast(float, ascr.degrees) - ayanamsa)

    asc_h, asc_adv_by = divmod(asc, 30)
    rasi_num = normalize_rasi(int(asc_h))
    rasi_occupied = Rasis(rasi_num if asc_adv_by == 0 else int(rasi_num + 1))
    posited_at = Houses.HOUSE1
    advanced_by = Angle(degrees=asc_adv_by)

    return PlanetPosition(
        "ascendant",
        Angle(degrees=0),
        Angle(degrees=asc),
        posited_at=posited_at,
        advanced_by=advanced_by,
        is_ascendant=True,
        rasi_occupied=rasi_occupied,
    )


def normalize_degree(degree: float) -> float:
    """Normalize the degree to be within 0-360.

    Args:
        degree (float): The degree to normalize.

    Returns:
        float: The normalized degree.

    """
    if degree < 0:
        return degree + DEGREE_MAX
    while degree > DEGREE_MAX:
        degree -= DEGREE_MAX
    return degree


def normalize_rasi(position: int) -> int:
    """Normalize the rasi position to be within 1-12.

    Args:
        position (int): The rasi position to normalize.

    Returns:
        int: The normalized rasi position.

    """
    if position < 0:
        return position + 12
    while position > 12:
        position -= 12
    return position


def get_all_planets_posited_in(rasi: Rasis, planets: list[PlanetPosition]) -> list[PlanetPosition] | None:
    """Get all the planets posited in the given rasi.

    Args:
        rasi (Rasis): The rasi to check.
        planets (list[PlanetPosition]): The list of planets.

    Returns:
        list[PlanetPosition] | None: A list of planets posited in the given rasi, or None if none are found.

    """
    for pos in planets:
        pass
    return []


def get_kattams(lat: Angle, lon: Angle, given_time: datetime) -> list[Kattam]:
    """Return the kattams for the given datetime, latitude, and longitude.

    Args:
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        given_time (datetime): The datetime of the observation.

    Returns:
        list[Kattam]: A list of kattams.

    """
    ayanamsa = get_lahiri_ayanamsa((cast(int, datetime.year), cast(int, datetime.month), cast(int, datetime.day)))
    ascendant = get_sidereal_ascendant_position(given_time, lat, lon, ayanamsa)
    planets = get_sidereal_planet_positions(lat, lon, given_time, ayanamsa)

    return []
