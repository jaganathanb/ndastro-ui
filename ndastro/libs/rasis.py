"""Define rasis for the ndastro.

Raises:
TypeError: _description_

Returns:
_type_: _description_

"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from ndastro.libs.constants import SYMBOLS
from ndastro.libs.errors import INVALID_DMS
from ndastro.libs.utils import deg_to_dms, sign


@dataclass
class DegMinSec:
    """Defines degree, minute & second."""

    degree: int
    minute: int
    second: int

    def format(self) -> str:
        """Format the DMS with symbols.

        Returns:
            str: The formatted dms string

        """
        return f"{self.degree}{SYMBOLS.DEGREE_SYMBOL}{self.minute}{SYMBOLS.MINUTE_SYMBOL}{self.second}{SYMBOLS.SECOND_SYMBOL}"

    def to_decimal(self) -> float:
        """Convert DegMinSec to decimal.

        Returns:
            float: The decimal from the DMS

        """
        return sign(self.degree) * (abs(self.degree) + self.minute / 60 + self.second / 3600)


@dataclass
class Rasi:
    """Defines rasi.

    Raises:
        TypeError: INVALID_DMS

    Returns:
        Rasi: The rasi

    """

    name: str
    symbol: str

    _start: DegMinSec
    _end: DegMinSec

    @property
    def start(self) -> DegMinSec:
        """Returns starting point of the rasi in DMS.

        Returns:
            DegMinSec: Degree, minute & second

        """
        return self._start

    @start.setter
    def start(self, dms: DegMinSec) -> None:
        if not isinstance(dms, DegMinSec):
            raise TypeError(INVALID_DMS)
        self.start = dms

    @property
    def end(self) -> DegMinSec:
        """Returns end point of the rasi in DMS.

        Returns:
            DegMinSec: Degree, minute & second

        """
        return self._end

    @end.setter
    def end(self, dms: DegMinSec) -> None:
        if not isinstance(dms, DegMinSec):
            raise TypeError(INVALID_DMS)
        self.end = dms

    advanced_by: DegMinSec | None = None
    advanced_by_deg: str = ""


# List of rasis
RASIS = [
    Rasi("Aries", "Ar", DegMinSec(0, 0, 0), DegMinSec(29, 59, 59)),
    Rasi("Taurus", "Ta", DegMinSec(30, 0, 0), DegMinSec(59, 59, 59)),
    Rasi("Gemini", "Ge", DegMinSec(60, 0, 0), DegMinSec(89, 59, 59)),
    Rasi("Cancer", "Cn", DegMinSec(90, 0, 0), DegMinSec(119, 59, 59)),
    Rasi("Leo", "Le", DegMinSec(120, 0, 0), DegMinSec(149, 59, 59)),
    Rasi("Virgo", "Vi", DegMinSec(150, 0, 0), DegMinSec(179, 59, 59)),
    Rasi("Libra", "Li", DegMinSec(180, 0, 0), DegMinSec(209, 59, 59)),
    Rasi("Scorpio", "Sc", DegMinSec(210, 0, 0), DegMinSec(239, 59, 59)),
    Rasi("Sagittarius", "Sg", DegMinSec(240, 0, 0), DegMinSec(269, 59, 59)),
    Rasi("Capricorn", "Cp", DegMinSec(270, 0, 0), DegMinSec(299, 59, 59)),
    Rasi("Aquarius", "Aq", DegMinSec(300, 0, 0), DegMinSec(329, 59, 59)),
    Rasi("Pisces", "Pi", DegMinSec(330, 0, 0), DegMinSec(359, 59, 59)),
]


def get_rasi_by_dms(dms: DegMinSec) -> Rasi | None:
    """Get rasi by given degree, minute & seconds.

    Args:
        dms (DegMinSec): The DMS to get the rasi

    Returns:
        Rasi | None: The conrresponding rasi for the given DSM or None

    """
    for rasi in RASIS:
        start_deg = sign(rasi.start.degree) * (abs(rasi.start.degree) + rasi.start.minute / 60 + rasi.start.second / 3600)
        end_deg = sign(rasi.end.degree) * (abs(rasi.end.degree) + rasi.end.minute / 60 + rasi.end.second / 3600)
        deg = sign(dms.degree) * (abs(dms.degree) + dms.minute / 60 + dms.second / 3600)

        if start_deg <= deg and end_deg >= deg:
            n_rasi = deepcopy(rasi)
            d, m, s = deg_to_dms(deg - start_deg)
            n_rasi.advanced_by = DegMinSec(d, m, s)
            n_rasi.advanced_by_deg = n_rasi.advanced_by.format()

            return n_rasi

    return None
