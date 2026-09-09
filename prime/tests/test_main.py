import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (2, True),
    (3, True),
    (10, False),
    (11, True),
    (27, False),
    (31, True),
    (55, False),
    (67, True),
]


@pytest.mark.parametrize('n, expected', testdata)
def test_run(n, expected):
    assert main.run(n) == expected
