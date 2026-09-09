import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (1, 0.4056959714),
    (0.25, 0.0253559982),
    (9.99, 40.4884985192),
]


@pytest.mark.parametrize('arc_A, expected', testdata)
def test_run(arc_A, expected):
    assert main.run(arc_A) == expected
