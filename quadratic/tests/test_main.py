import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (4, -6, 2, (1.0, 0.5)),
    (1, 2, -3, (1.0, -3.0)),
    (-1, -2, 8, (-4.0, 2.0)),
]


@pytest.mark.parametrize('a, b, c, expected', testdata)
def test_run(a, b, c, expected):
    assert main.run(a, b, c) == expected
