"""Module is to hold planet enums."""

from enum import IntEnum

from i18n import t


class Planets(IntEnum):
    """Enum to hold planets."""

    EMPTY = -1
    ASCENDANT = 0
    SUN = 1
    MOON = 2
    MARS = 3
    MERCURY = 4
    JUPITER = 5
    VENUS = 6
    SATURN = 7
    RAHU = 8
    KETHU = 9

    @staticmethod
    def to_string(num: int) -> str:
        """Convert planet number to display name of the planet.

        Args:
            num (int): the planet number

        Returns:
            str: return the planet name

        """
        return t(f"core.planets.planet{num}")

    @staticmethod
    def to_list() -> list[str]:
        """Convert planet enum to list of planet name.

        Returns:
            list[str]: list of planet names

        """
        return [el.name for el in Planets]
