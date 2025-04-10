"""Custom exceptions for handling errors related to dasha systems.

This module provides:
- UnsupportedDashaSystemError: Raised for unsupported dasha systems.
- MissingPlanetsPeriodError: Raised when planets period data is missing in dasha details.
"""

from ndastro.gui.models.dasha_detail import Dashas


class UnsupportedDashaSystemError(Exception):
    """Exception raised for unsupported dasha systems."""

    def __init__(self, dasha_system: Dashas) -> None:
        """Initialize the exception with the unsupported dasha system.

        Args:
            dasha_system (Dashas): The unsupported dasha system that caused the exception.

        """
        super().__init__(f"Unsupported dasha system: {dasha_system}")


class MissingPlanetsPeriodError(Exception):
    """Exception raised when planets period data is missing in dasha details."""

    def __init__(self) -> None:
        """Initialize the exception with a default message."""
        super().__init__("Planets period data is missing in dasha details")


class UnableToDetermineDashaError(Exception):
    """Exception raised when the running dasha cannot be determined."""

    def __init__(self):
        super().__init__("Unable to determine the running dasha")
