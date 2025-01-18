"""Test the RASI functionalities."""

import pytest

from ndastro.libs.constants import SYMBOLS
from ndastro.libs.rasis import RASIS, DegMinSec, Rasi, get_rasi_by_dms


@pytest.mark.parametrize(("test_input", "expected"), [(DegMinSec(94, 19, 0), RASIS[3])])
def test_get_rasi_by_dms(test_input: DegMinSec, expected: Rasi) -> None:
    rasi = get_rasi_by_dms(test_input)

    assert rasi is not None
    assert rasi.name == expected.name
    assert rasi.advanced_by_deg == f"4{SYMBOLS.DEGREE_SYMBOL}18{SYMBOLS.MINUTE_SYMBOL}59{SYMBOLS.SECOND_SYMBOL}"
