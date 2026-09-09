import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ('pypas 0.1.18', (5, 4)),
    ('Michael Jordan: 23', (13, 2)),
    ('Estrella Polar', (13, 0)),
    ('25/05/1977', (0, 8)),
    ('1.21 gigawatios', (10, 3)),
]


@pytest.mark.parametrize('text, expected', testdata)
def test_run(text, expected):
    assert main.run(text) == expected
