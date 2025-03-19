from datetime import datetime

import pytz
from skyfield.units import Angle

from ndastro.libs.retrograde import is_planet_in_retrograde


def test_is_planet_in_retrograde_true():
    check_date = datetime(2025, 4, 1, tzinfo=pytz.timezone("Asia/Kolkata"))
    planet_name = "venus"
    latitude = Angle(degrees=12.59)
    longitude = Angle(degrees=77.35)
    assert is_planet_in_retrograde(check_date, planet_name, latitude, longitude) is True


def test_is_planet_in_retrograde_false():
    check_date = datetime(2025, 1, 1, tzinfo=pytz.timezone("Asia/Kolkata"))
    planet_name = "venus"
    latitude = Angle(degrees=12.59)
    longitude = Angle(degrees=77.35)
    assert is_planet_in_retrograde(check_date, planet_name, latitude, longitude) is False


def test_is_planet_in_retrograde_edge_case_start():
    check_date = datetime(2023, 7, 24, tzinfo=pytz.timezone("Asia/Kolkata"))
    planet_name = "venus"
    latitude = Angle(degrees=12.59)
    longitude = Angle(degrees=77.35)
    assert is_planet_in_retrograde(check_date, planet_name, latitude, longitude) is True


def test_is_planet_in_retrograde_edge_case_end():
    check_date = datetime(2025, 9, 6, tzinfo=pytz.timezone("Asia/Kolkata"))
    planet_name = "venus"
    latitude = Angle(degrees=12.59)
    longitude = Angle(degrees=77.35)
    assert is_planet_in_retrograde(check_date, planet_name, latitude, longitude) is False


def test_is_planet_in_retrograde_invalid_date():
    check_date = datetime(1900, 1, 1, tzinfo=pytz.timezone("Asia/Kolkata"))
    planet_name = "venus"
    latitude = Angle(degrees=12.59)
    longitude = Angle(degrees=77.35)
    assert is_planet_in_retrograde(check_date, planet_name, latitude, longitude) is False
