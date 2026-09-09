import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ([[6, 4], [8, 9]], [[3, 2], [1, 7]], [[22, 40], [33, 79]]),
    ([[2, 0], [0, 2]], [[1, 0], [0, 1]], [[2, 0], [0, 2]]),
    ([[9, 7], [3, 2]], [[8, 4], [7, 3]], [[121, 57], [38, 18]]),
]


@pytest.mark.parametrize('A, B, expected', testdata)
def test_run(A, B, expected):
    assert main.run(A, B) == expected
