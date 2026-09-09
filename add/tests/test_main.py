import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (1, 1, 2),
    (-1, 1, 0),
    (9, 5, 14),
    (2, 8, 10),
]


@pytest.mark.parametrize('a, b, expected', testdata)
def test_run(a, b, expected):
    assert main.run(a, b) == expected
