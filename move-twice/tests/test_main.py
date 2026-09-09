import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (3, 6, 15),
    (1, 4, 9),
    (5, 2, 9),
]


@pytest.mark.parametrize('current_pos, dice, expected', testdata)
def test_run(current_pos, dice, expected):
    assert main.run(current_pos, dice) == expected
