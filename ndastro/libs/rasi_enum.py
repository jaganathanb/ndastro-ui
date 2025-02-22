"""Module to hold Rasi enums."""

from enum import IntEnum

from i18n import t


class Rasis(IntEnum):
    """Enum to represent Rasis."""

    ARIES = 1
    TAURUS = 2
    GEMINI = 3
    CANCER = 4
    LEO = 5
    VIRGO = 6
    LIBRA = 7
    SCORPIO = 8
    SAGITTARIUS = 9
    CAPRICORN = 10
    AQUARIUS = 11
    PISCES = 12

    def __str__(self) -> str:
        """Return a localized string representation of the Rasi.

        Returns:
            str: Localized name of the Rasi.

        """
        return t(f"core.rasis.rasi{self.value}")

    @classmethod
    def from_string(cls, rasi: str) -> "Rasis":
        """Convert a Rasi name to its corresponding enum member.

        Args:
            rasi (str): The name of the Rasi.

        Returns:
            Rasis: The corresponding enum member.

        """
        return cls[rasi.upper()]

    @classmethod
    def to_string(cls) -> str:
        """Convert a Rasi enum member to its localized display name.

        Returns:
            str: Localized name of the Rasi.

        """
        return t(f"core.rasis.rasi{cls.value}")

    @staticmethod
    def to_list() -> list[str]:
        """Get a list of all Rasi names.

        Returns:
            list[str]: List of all Rasi names.

        """
        return [el.name for el in Rasis]

    @staticmethod
    def to_4x4list() -> list[list[str]]:
        """Get a 4x4 grid representation of Rasi names.

        Returns:
            list[list[str]]: 4x4 grid of Rasi names.

        """
        rasis = Rasis.to_list()

        return [
            [rasis[11], rasis[0], rasis[1], rasis[2]],
            [rasis[10], "", "", rasis[3]],
            [rasis[9], "", "", rasis[4]],
            [rasis[8], rasis[7], rasis[6], rasis[5]],
        ]
