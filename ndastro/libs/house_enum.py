"""Module is to hold enums."""

from enum import IntEnum

from i18n import t


class Houses(IntEnum):
    """Enum to hold houses."""

    HOUSE1 = 1
    HOUSE2 = 2
    HOUSE3 = 3
    HOUSE4 = 4
    HOUSE5 = 5
    HOUSE6 = 6
    HOUSE7 = 7
    HOUSE8 = 8
    HOUSE9 = 9
    HOUSE10 = 10
    HOUSE11 = 11
    HOUSE12 = 12

    def __str__(self) -> str:
        """Return name of the house.

        Returns:
            str: name of the house

        """
        return t("core.house", num=self.value)
