from datetime import datetime
from typing import cast

import pytz
from skyfield.units import Angle

from ndastro.libs.constants import AYANAMSA
from ndastro.libs.utils import (
    calculate_lunar_nodes,
    get_sidereal_ascendant_position,
    get_sidereal_planet_positions,
    get_tropical_ascendant_position,
    get_tropical_planetary_positions,
    get_tropical_position_of,
)


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
        AYANAMSA.LAHIRI,
    )

    assert planet_pos is not None
    assert len(planet_pos) == 10
    for pos in planet_pos:
        rasi_occupied_str = str(pos.rasi_occupied) if pos.rasi_occupied is not None else "Unknown"
        print(
            f"The {pos.name} is in {rasi_occupied_str} rasi, advanced by {cast(Angle, pos.advanced_by).dstr(format='{0!s}{1!s}°{2:02}\'{3:02}.{4:0{5}}"')}",
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
    rasi_occupied_str = str(pos.rasi_occupied) if pos.rasi_occupied is not None else "Unknown"
    print(f"S Ascendant is in {rasi_occupied_str} rasi, advanced by {cast(Angle, pos.advanced_by).dstr(format='{0}{1}°{2:02}\'{3:02}.{4:0{5}}"')}")
