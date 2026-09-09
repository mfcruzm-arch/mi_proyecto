import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (1.08, 30.0),
    (4.25, 118.0),
    (0.099, 2.0),
]


@pytest.mark.parametrize('speed_km_h, expected', testdata)
def test_run(speed_km_h, expected):
    assert main.run(speed_km_h) == expected
