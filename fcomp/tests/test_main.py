import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (0, 10, [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32]),
    (-7, 0, [-19, -16, -13, -10, -7, -4, -1, 2]),
    (131, 134, [395, 398, 401, 404]),
    (0, 1, [2, 5]),
]


@pytest.mark.parametrize('xmin, xmax, expected', testdata)
def test_run(xmin, xmax, expected):
    assert main.run(xmin, xmax) == expected
