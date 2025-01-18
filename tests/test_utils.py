from datetime import datetime
from typing import cast

import pytz
from skyfield.units import Angle

from ndastro.libs.constants import AYANAMSA
from ndastro.libs.utils import (
    calculate_lunar_nodes,
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
    assert len(planet_pos) == 14
    for pos in planet_pos:
        print(f"The {pos[0]}'s position is: {(cast(float, pos[2].degrees) - AYANAMSA.LAHIRI) % 360}")


def test_calculate_lunar_nodes() -> None:
    rahu, kethu = calculate_lunar_nodes(datetime.now(pytz.timezone("Asia/Kolkata")))

    assert "rahu" in rahu
    assert "kethu" in kethu
    print(rahu[2].degrees)
    print(kethu[2].degrees)
