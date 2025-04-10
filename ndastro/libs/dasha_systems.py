"""Provide classes and enumerations for managing dasha systems in Vedic astrology.

Includes:
- Dashas: An enumeration of different dasha systems.
- DashaSystem: A class to manage and provide details about various dasha systems.
"""

from datetime import datetime

from ndastro.gui.models.dasha_detail import DashaDetail, Dashas
from ndastro.libs.custom_errors import (
    MissingPlanetsPeriodError,
    UnableToDetermineDashaError,
    UnsupportedDashaSystemError,
)
from ndastro.libs.planet_enum import Planets


class DashaSystem:
    """A class to manage and provide details about various dasha systems in Vedic astrology."""

    def __init__(self) -> None:
        """Initialize the DashaSystem class with a list of available dasha systems."""
        self.available_systems = [Dashas.VIMSHOTTARI, Dashas.ASHTOTTARI, Dashas.KALACHAKRA]

    def get_all_dasha_systems(self) -> list[Dashas]:
        """Return list of all available dasha systems."""
        return self.available_systems

    def get_vimshottari_details(self) -> DashaDetail:
        """Return the details of the Vimshottari dasha system."""
        return DashaDetail(
            name="Vimshottari",
            description="A widely used dasha system in Vedic astrology based on a 120-year cycle.",
            cycle_years=120,
            dasha_system=Dashas.VIMSHOTTARI,
            planets_period={
                Planets.KETHU: 7,
                Planets.VENUS: 20,
                Planets.SUN: 6,
                Planets.MOON: 10,
                Planets.MARS: 7,
                Planets.RAHU: 18,
                Planets.JUPITER: 16,
                Planets.SATURN: 19,
                Planets.MERCURY: 17,
            },
        )

    def get_ashtottari_details(self) -> DashaDetail:
        """Return the details of the Ashtottari dasha system."""
        return DashaDetail(
            name="Ashtottari",
            description="A dasha system based on a 108-year cycle, used in specific astrological contexts.",
            cycle_years=108,
            dasha_system=Dashas.ASHTOTTARI,
            planets_period={
                Planets.KETHU: 7,
                Planets.VENUS: 20,
                Planets.SUN: 6,
                Planets.MOON: 10,
                Planets.MARS: 7,
                Planets.RAHU: 18,
                Planets.JUPITER: 16,
                Planets.SATURN: 19,
                Planets.MERCURY: 5,
            },
        )

    def get_kalachakra_details(self) -> DashaDetail:
        """Return the details of the Kalachakra dasha system."""
        return DashaDetail(
            name="Kalachakra",
            description="A complex dasha system based on the Kalachakra mandala.",
            dasha_system=Dashas.KALACHAKRA,
            cycle_years=28,
            planets_period={
                Planets.MOON: 1,
                Planets.MARS: 2,
                Planets.MERCURY: 3,
                Planets.VENUS: 4,
                Planets.JUPITER: 5,
                Planets.SUN: 6,
                Planets.SATURN: 7,
            },
        )

    def find_running_dasha(self, birth_datetime: datetime, current_datetime: datetime, dasha_system: Dashas) -> Planets:
        """Find the running dasha for the given birth and current datetime in the specified dasha system.

        This method calculates the currently active dasha (planetary period) based on the individual's
        birth date and time, the current date and time, and the specified dasha system. It supports
        multiple dasha systems such as Vimshottari, Ashtottari, and Kalachakra.
            dasha_system (Dashas): The dasha system to use for calculation. Must be one of the supported
                dasha systems (e.g., Dashas.VIMSHOTTARI, Dashas.ASHTOTTARI, Dashas.KALACHAKRA).
            Planets: The planet corresponding to the currently running dasha.

        Raises:
            UnsupportedDashaSystemError: If the provided dasha system is not supported.
            MissingPlanetsPeriodError: If the dasha system does not have planet-period mappings.
            UnableToDetermineDashaError: If the running dasha cannot be determined due to unexpected conditions.

        """
        # Get the dasha details based on the selected system
        if dasha_system == Dashas.VIMSHOTTARI:
            dasha_details = self.get_vimshottari_details()
        elif dasha_system == Dashas.ASHTOTTARI:
            dasha_details = self.get_ashtottari_details()
        elif dasha_system == Dashas.KALACHAKRA:
            dasha_details = self.get_kalachakra_details()
        else:
            raise UnsupportedDashaSystemError(dasha_system)

        # Calculate the total elapsed time in days
        total_days = (current_datetime - birth_datetime).days

        # Convert the cycle years to days
        cycle_days = dasha_details.cycle_years * 365

        # Find the position within the cycle
        position_in_cycle = total_days % cycle_days

        # Iterate through the planets and their periods to find the running dasha
        if not dasha_details.planets_period:
            raise MissingPlanetsPeriodError

        elapsed_days = 0
        for planet, period_years in dasha_details.planets_period.items():
            period_days = period_years * 365
            if elapsed_days + period_days > position_in_cycle:
                return planet
            elapsed_days += period_days

        raise UnableToDetermineDashaError
