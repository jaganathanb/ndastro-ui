"""Module is to hold start enums."""

from enum import Enum

from i18n import t


class Natchaththirams(Enum):
    """Enum to hold stars."""

    ASWINNI = 1
    BHARANI = 2
    KAARTHIKAI = 3
    ROGHINI = 4
    MIRUGASIRISAM = 5
    THIRUVAATHIRAI = 6
    PUNARPOOSAM = 7
    POOSAM = 8
    AAYILYAM = 9
    MAGAM = 10
    POORAM = 11
    UTHTHIRAM = 12
    ASTHTHAM = 13
    CHITHTHIRAI = 14
    SUVAATHI = 15
    VISAAGAM = 16
    ANUSHAM = 17
    KETTAI = 18
    MOOLAM = 19
    POORAADAM = 20
    UTHTHIRAADAM = 21
    THIRUVONAM = 22
    AVITTAM = 23
    SHATHAYAM = 24
    POORATTAATHI = 25
    UTHTHIRATTAATHI = 26
    REVATHI = 27

    def __str__(self) -> str:
        """Return the display name of the star.

        Returns:
            str: The display name of the star.

        """
        return t(f"core.stars.star{self.value}")

    @staticmethod
    def to_string(num: int) -> str:
        """Convert star number to display name of the star.

        Args:
            num (int): the star number

        Returns:
            str: return the star name

        """
        return t(f"core.stars.star{num}")

    @staticmethod
    def to_list() -> list[str]:
        """Convert enum to list of enum item name.

        Returns:
            list[str]: list of enum item name

        """
        return [el.name for el in Natchaththirams]
