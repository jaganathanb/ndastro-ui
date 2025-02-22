"""Module is to hold start enums."""

from enum import Enum

from i18n import t


class Stars(Enum):
    """Enum to hold stars."""

    ASWINNI = 1
    BHARANI = 2
    KRITTIKA = 3
    ROHINI = 4
    MRIGASHIRA = 5
    ARDRA = 6
    PUNURVASU = 7
    PUSHYAMI = 8
    ASLESHA = 9
    MAGHA = 10
    PURVAPHALGUNI = 11
    UTTARAPHALGUNI = 12
    HASTA = 13
    CHITRA = 14
    SVATI = 15
    VISHAKA = 16
    ANURADHA = 17
    JYESTA = 18
    MOOLA = 19
    PURVAASHADA = 20
    UTTARAASHADA = 21
    SRAVANA = 22
    DHANISHTA = 23
    SHATABISHAK = 24
    PURVABHADRA = 25
    UTTARABHADRA = 26
    REVATI = 27

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
        return [el.name for el in Stars]
