"""Module to hold all the util defs."""

from __future__ import annotations

from datetime import datetime, timedelta
from math import atan2, ceil, cos, degrees, floor, radians, sin, tan
from typing import TYPE_CHECKING, cast

from skyfield.almanac import sunrise_sunset
from skyfield.searchlib import find_discrete
from skyfield.timelib import Time

from ndastro.gui.models.planet_position import PlanetDetail
from ndastro.libs.nakshatra_enum import Natchaththirams
from ndastro.libs.planet_enum import Planets
from ndastro.libs.retrograde import is_planet_in_retrograde

if TYPE_CHECKING:
    from ndastro.gui.models.kattam import Kattam

from skyfield.api import load
from skyfield.data.spice import inertial_frames
from skyfield.elementslib import osculating_elements_of
from skyfield.nutationlib import mean_obliquity
from skyfield.positionlib import Barycentric
from skyfield.toposlib import Topos
from skyfield.units import Angle, Distance
from skyfield.vectorlib import VectorSum

from ndastro.libs.ayanamsa import get_lahiri_ayanamsa
from ndastro.libs.constants import (
    AYANAMSA,
    DEGREE_MAX,
    DEGREES_PER_RAASI,
    TOTAL_RAASI,
)
from ndastro.libs.house_enum import Houses
from ndastro.libs.rasi_enum import Rasis

if TYPE_CHECKING:
    from ndastro.gui.models.kattam import Kattam

from ndastro.libs.constants import TOTAL_NAKSHATRAS

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


def dms_to_decimal(degrees: int, minutes: int, seconds: float) -> float:
    """Convert degrees, minutes, and seconds to decimal degrees.

    Args:
        degrees (int): The degrees part.
        minutes (int): The minutes part.
        seconds (float): The seconds part.

    Returns:
        float: The decimal degrees.

    """
    return degrees + minutes / 60 + seconds / 3600


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


def get_tropical_planetary_positions(lat: Angle, lon: Angle, given_time: datetime) -> list[PlanetDetail]:
    """Return the tropical positions of the planets.

    Args:
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        given_time (datetime): The datetime of the observation.

    Returns:
        list[PlanetDetail]: A list of tropical positions of the planets.

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
    positions: list[PlanetDetail] = []

    for planet_name, planet_code in planets.items():
        if planet_code == "rahu":
            nodes = calculate_lunar_nodes(given_time)
            positions.extend(nodes)
            continue

        lat, lon, distance = get_tropical_position_of(planet_code, lat, lon, given_time)

        positions.append(
            PlanetDetail(
                planet_name,
                lat,
                lon,
                distance=distance,
            ),
        )

    return positions


def calculate_lunar_nodes(given_time: datetime) -> list[PlanetDetail]:
    """Calculate the positions of the lunar nodes.

    Args:
        given_time (datetime): The datetime of the observation.

    Returns:
        list[PlanetDetail]: A list containing the positions of Rahu and Kethu.

    """
    t = ts.utc(given_time)
    ecliptic = inertial_frames["ECLIPJ2000"]

    earth = eph["earth"]
    moon = eph["moon"]
    position = cast(VectorSum, (moon - earth)).at(t)
    elements = osculating_elements_of(position, ecliptic)

    rahu_position = cast(float, cast(Angle, elements.longitude_of_ascending_node).degrees)
    kethu_position = normalize_degree(rahu_position + 180)

    declination_placeholder = 0.0

    return [
        PlanetDetail(
            "rahu",
            Angle(degrees=declination_placeholder),
            Angle(degrees=rahu_position),
        ),
        PlanetDetail(
            "kethu",
            Angle(degrees=declination_placeholder),
            Angle(degrees=kethu_position),
        ),
    ]


def get_sidereal_planet_positions(lat: Angle, lon: Angle, given_time: datetime, ayanamsa: float) -> list[PlanetDetail]:
    """Return the sidereal positions of the planets.

    Args:
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        given_time (datetime): The datetime of the observation.
        ayanamsa (float): The ayanamsa value to be used for calculation.

    Returns:
        list[PlanetDetail]: A list of sidereal positions of the planets.

    """
    positions = get_tropical_planetary_positions(lat, lon, given_time)
    asc_pos = get_sidereal_ascendant_position(given_time, lat, lon, ayanamsa)

    for pos in positions:
        asc = normalize_degree(cast(float, pos.longitude.degrees) - ayanamsa)

        asc_h, asc_adv_by = divmod(asc, DEGREES_PER_RAASI)
        rasi_num = int(asc_h)

        pos.nirayana_longitude = Angle(degrees=asc)
        pos.rasi_occupied = Rasis(normalize_rasi_house(rasi_num if asc_adv_by == 0 else int(rasi_num + 1)))
        pos.house_posited_at = cast(
            Houses,
            normalize_rasi_house(cast(Houses, asc_pos.house_posited_at) + Houses(rasi_num)),
        )
        pos.advanced_by = Angle(degrees=asc_adv_by)

        nakshatra, pada = get_nakshatra_and_pada(Angle(degrees=asc))
        pos.natchaththiram = nakshatra
        pos.paatham = pada

        pos.retrograde = (
            True if pos.planet.code in [Planets.RAHU.code, Planets.KETHU.code] else is_planet_in_retrograde(given_time, pos.planet.code, lat, lon)
        )

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

    return Angle(degrees=normalize_degree(asc))


def get_sidereal_ascendant_position(given_time: datetime, lat: Angle, lon: Angle, ayanamsa: float = AYANAMSA.LAHIRI) -> PlanetDetail:
    """Calculate the sidereal ascendant.

    Args:
        given_time (datetime): The datetime of the observation.
        lat (Angle): The latitude of the observer.
        lon (Angle): The longitude of the observer.
        ayanamsa (float): The ayanamsa value to be used for calculation.

    Returns:
        PlanetDetail: The position of the sidereal ascendant.

    """
    ascr = get_tropical_ascendant_position(given_time, lat, lon)

    asc = normalize_degree(cast(float, ascr.degrees) - ayanamsa)

    asc_h, asc_adv_by = divmod(asc, 29.99972222)
    rasi_num = int(asc_h)
    rasi_occupied = Rasis(normalize_rasi_house(rasi_num if asc_adv_by == 0 else int(rasi_num + 1)))
    posited_at = Houses.HOUSE1
    advanced_by = Angle(degrees=asc_adv_by)

    nakshatra, pada = get_nakshatra_and_pada(Angle(degrees=asc))

    return PlanetDetail(
        "ascendant",
        Angle(degrees=0),
        ascr,
        nirayana_longitude=Angle(degrees=asc),
        house_posited_at=posited_at,
        advanced_by=advanced_by,
        is_ascendant=True,
        natchaththiram=nakshatra,
        paatham=pada,
        rasi_occupied=rasi_occupied,
    )


def get_nakshatra_and_pada(longitude: Angle) -> tuple[Natchaththirams, int]:
    """Get the nakshatra and pada from the planet longitude.

    Args:
        longitude (Angle): The longitude of the planet.

    Returns:
        tuple[str, int]: The nakshatra and pada.

    """
    degrees_per_nakshatra = Angle(degrees=DEGREE_MAX / TOTAL_NAKSHATRAS)

    total_degrees_mins = cast(float, longitude.arcminutes())

    nakshatra_index = total_degrees_mins / degrees_per_nakshatra.arcminutes()

    remainder = nakshatra_index - floor(nakshatra_index)
    pada_threshold_1 = 0.25
    pada_threshold_2 = 0.5
    pada_threshold_3 = 0.75

    if remainder < pada_threshold_1:
        pada = 1
    elif remainder < pada_threshold_2:
        pada = 2
    elif remainder < pada_threshold_3:
        pada = 3
    else:
        pada = 4

    nakshatra = Natchaththirams(ceil(nakshatra_index + 1 if nakshatra_index == 0 else nakshatra_index))

    return nakshatra, pada


def get_sunrise_sunset(lat: Angle, lon: Angle, given_time: datetime) -> tuple[datetime, datetime]:
    """Calculate the sunrise and sunset times for a given location and date.

    Args:
        lat (Angle): The latitude of the location.
        lon (Angle): The longitude of the location.
        given_time (datetime): The date and time for which to calculate the sunrise and sunset times.

    Returns:
        tuple[datetime, datetime]: A tuple containing the sunrise and sunset times as datetime objects.

    """
    # Define location
    location = Topos(latitude_degrees=lat.degrees, longitude_degrees=lon.degrees)

    # Define time range for the search (e.g., one day)
    t_start = ts.utc(given_time.date())  # Start of the day
    t_end = ts.utc(given_time.date() + timedelta(days=1))  # End of the day

    # Find sunrise time
    f = sunrise_sunset(eph, location)
    times, events = find_discrete(t_start, t_end, f)

    sunrise, sunset = cast(list[Time], [time for time, _ in zip(times, events)])

    return cast(tuple[datetime, datetime], (sunrise.utc_datetime(), sunset.utc_datetime()))


def normalize_degree(degree: float) -> float:
    """Normalize the degree to be within 0-360.

    Args:
        degree (float): The degree to normalize.

    Returns:
        float: The normalized degree.

    """
    if degree < 0:
        return DEGREE_MAX + degree
    while degree > DEGREE_MAX:
        degree -= DEGREE_MAX
    return degree


def normalize_rasi_house(position: int) -> int:
    """Normalize the rasi position to be within 1-12.

    Args:
        position (int): The rasi position to normalize.

    Returns:
        int: The normalized rasi position.

    """
    if position < 0:
        return TOTAL_RAASI + position
    while position > TOTAL_RAASI:
        position -= TOTAL_RAASI
    return position


def get_all_planets_posited_in(rasi: Rasis, planets: list[PlanetDetail]) -> list[PlanetDetail] | None:
    """Get all the planets posited in the given rasi.

    Args:
        rasi (Rasis): The rasi to check.
        planets (list[PlanetDetail]): The list of planets.

    Returns:
        list[PlanetDetail] | None: A list of planets posited in the given rasi, or None if none are found.

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
    ayanamsa = get_lahiri_ayanamsa(given_time)
    ascendant = get_sidereal_ascendant_position(given_time, lat, lon, ayanamsa)
    planets = get_sidereal_planet_positions(lat, lon, given_time, ayanamsa)

    return []
