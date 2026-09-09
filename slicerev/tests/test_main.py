import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ([5, 4, 3, 9, 7, 1, 1, 1, 8, 6], [6, 8, 1, 1, 1, 7, 9, 3, 4, 5]),
    ([4, 3, 8, 3, 1, 7], [3, 4]),
    ([2, 8, 7, 9, 3, 2, 7, 4, 3, 7, 5, 6, 4, 6, 3, 1], [1, 4, 7, 7, 9, 2]),
    ([1, 5, 3], [1]),
    ([8, 2], [8]),
    ([1], [1]),
    ([], []),
]


@pytest.mark.parametrize('items, expected', testdata)
def test_run(items, expected):
    assert main.run(items) == expected  # type: ignore
