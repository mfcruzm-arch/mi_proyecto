import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (10, 5, 30, 4740.0),
    (2, 1.5, 50, 150.0),
    (5, 2.25, 75, 1125.0),
]


@pytest.mark.parametrize('num_pillars, gap_pillars, pillar_width, expected', testdata)
def test_run(num_pillars, gap_pillars, pillar_width, expected):
    assert main.run(num_pillars, gap_pillars, pillar_width) == expected
