"""Module contains unit tests for various utility functions in the ndastro library."""

from datetime import datetime
from typing import cast

import pytest
import pytz
from skyfield.units import Angle

from ndastro.libs.ayanamsa import get_lahiri_ayanamsa
from ndastro.libs.constants import AYANAMSA
from ndastro.libs.nakshatra_enum import Natchaththirams
from ndastro.libs.planet_enum import Planets
from ndastro.libs.utils import (
    calculate_lunar_nodes,
    dms_to_decimal,
    get_nakshatra_and_pada,
    get_sidereal_ascendant_position,
    get_sidereal_planet_positions,
    get_sunrise_sunset,
    get_tropical_ascendant_position,
    get_tropical_planetary_positions,
    get_tropical_position_of,
    is_planet_in_retrograde,
)


def test_dms_to_decimal() -> None:
    degrees, minutes, seconds = 13, 20, 0
    decimal_degrees = dms_to_decimal(degrees, minutes, seconds)
    expected = 13 + 20 / 60 + 0 / 3600
    assert decimal_degrees == expected, f"Expected {expected}, but got {decimal_degrees}"

    degrees, minutes, seconds = -12, 34, 56.78
    decimal_degrees = dms_to_decimal(degrees, minutes, seconds)
    expected = -12 + 34 / 60 + 56.78 / 3600
    assert decimal_degrees == expected, f"Expected {expected}, but got {decimal_degrees}"


def test_position_of() -> None:
    latitude, longitude = 12.9716, 77.5946  # Bengaluru, India
    lat, lon, dis = get_tropical_position_of(
        "moon",
        Angle(degrees=latitude),
        Angle(degrees=longitude),
        datetime.fromisoformat("2025-01-11T21:09:20+05:30"),
    )
    assert lat is not None
    assert lon is not None
    assert dis is not None

    print("Moon position is {lon}", cast(float, lon.degrees) - 24 % 360)


def test_get_tropical_planetary_positions() -> None:
    latitude, longitude = 12.9716, 77.5946  # Bengaluru, India
    planet_pos = get_tropical_planetary_positions(
        Angle(degrees=latitude),
        Angle(degrees=longitude),
        datetime.now(pytz.timezone("Asia/Kolkata")),
    )

    assert planet_pos is not None
    assert len(planet_pos) == 9
    for pos in planet_pos:
        print(f"The {pos.name}'s position is: {(cast(float, pos.longitude.degrees) - AYANAMSA.LAHIRI) % 360}")


def test_get_sidereal_planetary_positions() -> None:
    latitude, longitude = 12.59, 77.35  # Bengaluru, India
    planet_pos = get_sidereal_planet_positions(
        Angle(degrees=latitude),
        Angle(degrees=longitude),
        datetime.now(pytz.timezone("Asia/Kolkata")),
        get_lahiri_ayanamsa(datetime.now(pytz.timezone("Asia/Kolkata"))),
    )

    assert planet_pos is not None
    assert len(planet_pos) == 10
    for pos in planet_pos:
        rasi_occupied_str = str(pos.rasi_occupied) if pos.rasi_occupied is not None else "Unknown"
        print(
            f"The {pos.name} is in {rasi_occupied_str} rasi, advanced by "
            f"{cast(Angle, pos.advanced_by).dstr(format='{0!s}{1!s}°{2:02}\'{3:02}.{4:0{5}}"')} "
            f"at house {pos.house_posited_at} - total longitude = {cast(Angle, pos.nirayana_longitude).degrees}°",
            f"retrograde = {pos.retrograde}",
            f"nakshatra = {pos.natchaththiram} and pada = {pos.paatham}",
        )


def test_calculate_lunar_nodes() -> None:
    rahu, kethu = calculate_lunar_nodes(datetime.now(pytz.timezone("Asia/Kolkata")))

    assert rahu.name == "rahu"
    assert kethu.name == "kethu"
    print(rahu.longitude.degrees)
    print(kethu.longitude.degrees)


def test_get_tropical_ascendant_position() -> None:
    pos = get_tropical_ascendant_position(datetime.now(pytz.timezone("Asia/Kolkata")), Angle(degrees=12.59), Angle(degrees=77.35))
    house = cast(float, pos.degrees) // 30
    print(f"Ascendant is in {house}th rasi {pos.dstr()} {pos.dms()}")


def test_get_sidereal_ascendant_position() -> None:
    pos = get_sidereal_ascendant_position(datetime.now(pytz.timezone("Asia/Kolkata")), Angle(degrees=12.59), Angle(degrees=77.35))
    a = Angle(degrees=103.56)
    print(f"The DMS = {a.dstr(format='{0}{1}°{2:02}\'{3:02}.{4:0{5}}"')}")
    rasi_occupied_str = str(pos.rasi_occupied) if pos.rasi_occupied is not None else "Unknown"
    print(f"S Ascendant is in {rasi_occupied_str} rasi, advanced by {cast(Angle, pos.advanced_by).dstr(format='{0}{1}°{2:02}\'{3:02}.{4:0{5}}"')}")


@pytest.mark.parametrize(
    ("degrees", "expected_nakshatra", "expected_pada"),
    [
        (5, Natchaththirams.ASWINNI, 2),
        (13.3333334, Natchaththirams.BHARANI, 1),
        (26.6667, Natchaththirams.KAARTHIKAI, 1),
        (30, Natchaththirams.KAARTHIKAI, 2),
        (359.4, Natchaththirams.REVATHI, 4),
        (180, Natchaththirams.CHITHTHIRAI, 3),
        (270, Natchaththirams.UTHTHIRAADAM, 2),
    ],
)
def test_get_nakshatra_and_pada(degrees: float, expected_nakshatra: Natchaththirams, expected_pada: int) -> None:
    nakshatra, pada = get_nakshatra_and_pada(Angle(degrees=degrees))
    assert nakshatra.name == expected_nakshatra.name, f"Expected {expected_nakshatra}, but got {nakshatra}"
    assert pada == expected_pada, f"Expected {expected_pada}, but got {pada}"


@pytest.mark.parametrize(
    ("planet", "given_time", "expected"),
    [
        (Planets.SUN, datetime(2025, 4, 15, 21, 9, 20, tzinfo=pytz.timezone("Asia/Kolkata")), False),
        (Planets.MERCURY, datetime(2025, 3, 17, 21, 9, 20, tzinfo=pytz.timezone("Asia/Kolkata")), True),
        (Planets.VENUS, datetime(2025, 3, 30, 9, 9, 20, tzinfo=pytz.timezone("Asia/Kolkata")), True),
        (Planets.MARS, datetime(2025, 1, 11, 21, 9, 20, tzinfo=pytz.timezone("Asia/Kolkata")), True),
    ],
)
def test_is_planet_in_retrograde(planet: Planets, given_time: datetime, expected: bool) -> None:
    assert is_planet_in_retrograde(given_time, planet.code, Angle(degrees=12.59), Angle(degrees=77.35)) == expected, (
        f"Expected {planet.name} retrograde status to be {expected}"
    )


@pytest.mark.parametrize(
    ("latitude", "longitude", "given_time"),
    [
        (12.59, 77.35, datetime(2025, 1, 11, tzinfo=pytz.timezone("Asia/Kolkata"))),  # Bengaluru, India
        (12.59, 77.35, datetime(2025, 6, 21, tzinfo=pytz.timezone("Asia/Kolkata"))),  # Bengaluru, India
        (12.59, 77.35, datetime(2025, 12, 25, tzinfo=pytz.timezone("Asia/Kolkata"))),  # Bengaluru, India
    ],
)
def test_get_sunrise_sunset(latitude: float, longitude: float, given_time: datetime) -> None:
    sunrise, sunset = get_sunrise_sunset(Angle(degrees=latitude), Angle(degrees=longitude), given_time)

    assert sunrise is not None, "Sunrise time should not be None"
    assert sunset is not None, "Sunset time should not be None"
    assert sunrise < sunset, "Sunrise should be before sunset"

    sunrise_str = sunrise.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S IST")
    sunset_str = sunset.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S IST")
    print(f"Location ({latitude}, {longitude}) - Sunrise: {sunrise_str}, Sunset: {sunset_str}")
