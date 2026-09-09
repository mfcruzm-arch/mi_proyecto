import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (4, 50.24),
    (2, 12.56),
    (8.5, 226.865),
]


@pytest.mark.parametrize('radius, expected', testdata)
def test_result(radius, expected):
    assert main.run(radius) == expected
