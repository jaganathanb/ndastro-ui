from datetime import datetime

import pytest
import pytz
from pytest_mock import MockerFixture

from ndastro.gui.models.dasha_detail import Dashas
from ndastro.libs.custom_errors import (
    MissingPlanetsPeriodError,
    UnableToDetermineDashaError,
    UnsupportedDashaSystemError,
)
from ndastro.libs.dasha_systems import DashaSystem
from ndastro.libs.planet_enum import Planets


@pytest.fixture
def dasha_system() -> DashaSystem:
    return DashaSystem()


def test_find_running_dasha_vimshottari(dasha_system: DashaSystem) -> None:
    birth_datetime = datetime(1990, 1, 1, tzinfo=pytz.utc)
    current_datetime = datetime(2020, 1, 1, tzinfo=pytz.utc)
    running_dasha = dasha_system.find_running_dasha(
        birth_datetime,
        current_datetime,
        Dashas.VIMSHOTTARI,
    )
    assert running_dasha == Planets.MERCURY  # Expected based on Vimshottari periods


def test_find_running_dasha_ashtottari(dasha_system: DashaSystem):
    birth_datetime = datetime(1990, 1, 1, tzinfo=pytz.utc)
    current_datetime = datetime(2020, 1, 1, tzinfo=pytz.utc)
    running_dasha = dasha_system.find_running_dasha(
        birth_datetime,
        current_datetime,
        Dashas.ASHTOTTARI,
    )
    assert running_dasha == Planets.MERCURY  # Expected based on Ashtottari periods


def test_find_running_dasha_kalachakra(dasha_system: DashaSystem):
    birth_datetime = datetime(1990, 1, 1, tzinfo=pytz.utc)
    current_datetime = datetime(1995, 1, 1, tzinfo=pytz.utc)
    running_dasha = dasha_system.find_running_dasha(
        birth_datetime,
        current_datetime,
        Dashas.KALACHAKRA,
    )
    assert running_dasha == Planets.MARS  # Expected based on Kalachakra periods


def test_find_running_dasha_unsupported_system(dasha_system: DashaSystem):
    birth_datetime = datetime(1990, 1, 1, tzinfo=pytz.utc)
    current_datetime = datetime(2020, 1, 1, tzinfo=pytz.utc)
    with pytest.raises(UnsupportedDashaSystemError):
        dasha_system.find_running_dasha(
            birth_datetime,
            current_datetime,
            Dashas(10),  # Replace with a valid Dashas enum value for testing
        )


def test_find_running_dasha_missing_planets_period(dasha_system: DashaSystem, mocker: MockerFixture):
    mocker.patch.object(
        dasha_system,
        "get_vimshottari_details",
        return_value=mocker.Mock(planets_period=None),
    )
    birth_datetime = datetime(1990, 1, 1, tzinfo=pytz.utc)
    current_datetime = datetime(2020, 1, 1, tzinfo=pytz.utc)
    with pytest.raises(MissingPlanetsPeriodError):
        dasha_system.find_running_dasha(
            birth_datetime,
            current_datetime,
            Dashas.VIMSHOTTARI,
        )


def test_find_running_dasha_unable_to_determine(dasha_system: DashaSystem, mocker):
    mocker.patch.object(
        dasha_system,
        "get_vimshottari_details",
        return_value=mocker.Mock(planets_period={Planets.SUN: 5}),
    )
    birth_datetime = datetime(1990, 1, 1, tzinfo=pytz.utc)
    current_datetime = datetime(2020, 1, 1, tzinfo=pytz.utc)
    with pytest.raises(UnableToDetermineDashaError):
        dasha_system.find_running_dasha(
            birth_datetime,
            current_datetime,
            Dashas.VIMSHOTTARI,
        )
