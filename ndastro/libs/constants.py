"""Define all the constants needed for the ndastro libs."""

from os import name
from typing import Final


class SYMBOLS:
    """Unicode symbols used in astronomy."""

    DEGREE_SYMBOL = "\u00b0"
    MINUTE_SYMBOL = "\u2032"
    SECOND_SYMBOL = "\u2033"
    RETROGRADE_SYMBOL = "℞"
    ASENDENT_SYMBOL = "L"


class AYANAMSA:
    """Different Ayanamsas for the system."""

    CENTURY_19: Final[int] = 1900
    CENTURY_20: Final[int] = 2000
    CENTURY_21: Final[int] = 2100

    AYANAMSA_AT_J2000 = 22.460148
    DEG_PER_JCENTURY = 1.396042
    DEG_PER_SQUARE_JCENTURY = 0.000308

    LAHIRI = 24.12

    def __init__(self, name: str) -> None:
        """Set current active ayanamsa.

        Args:
            name (str): Name of the current active ayanams.

        """
        self._name = name

    @property
    def name(self) -> str:
        """Name of the active ayanamsa."""
        return self._name

    @property
    def value(self) -> float:
        """Return value of the active ayanamsa.

        Returns:
            value (float): Ayanamsa value

        """
        match name:
            case "lahiri":
                return self.LAHIRI
            case _:
                return self.LAHIRI

    @value.setter
    def value(self, val: float) -> None:
        match name:
            case "lahiri":
                self.LAHIRI = val
            case _:
                self.LAHIRI = 24
