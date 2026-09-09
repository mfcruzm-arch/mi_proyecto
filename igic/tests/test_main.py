import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (120, 7, 112.15),
    (50, 4.5, 47.85),
    (1500, 9.75, 1366.74),
]


@pytest.mark.parametrize('price_with_igic, igic, expected', testdata)
def test_run(price_with_igic, igic, expected):
    assert main.run(price_with_igic, igic) == expected
