from datetime import datetime

import pytz

from ndastro.libs.ayanamsa import (
    calculate_b6,
    get_days_in_julian_century,
    get_days_since_julian,
    get_lahiri_ayanamsa,
)


def test_get_lahiri_ayanamsa() -> None:
    value = get_lahiri_ayanamsa(datetime.now(pytz.timezone("Asia/Kolkata")))

    assert value is not None


def test_days_since_julian() -> None:
    expected = 2415021.0
    datetime.now(pytz.timezone("Asia/Kolkata"))
    days = get_days_since_julian(1900)

    assert days is not None
    assert days == expected


def test_get_days_in_julian_century() -> None:
    expected = 36524.0
    datetime.now(pytz.timezone("Asia/Kolkata"))
    days = get_days_in_julian_century(1900, 2000)

    assert days is not None
    assert days == expected


def test_calculate_b6() -> None:
    date = datetime.now(pytz.timezone("Asia/Kolkata"))
    b6 = calculate_b6((date.year, date.month, date.day))

    assert b6 is not None
