import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (90, 1.0),
    (45, 0.7058823529411765),
    (50, 0.7647058823529411),
]


@pytest.mark.parametrize('x, expected', testdata)
def test_run(x, expected):
    assert main.run(x) == expected
