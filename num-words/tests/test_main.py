import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ('Before software can be reusable it first has to be usable', 11),
    ('You should prefer readability over performance in almost all cases', 10),
    ('Models are not right or wrong they are more or less useful', 12),
    ('Simplicity is the soul of efficiency  ', 6),
    ('  Premature optimization is the root of all evil', 8),
]


@pytest.mark.parametrize('text, expected', testdata)
def test_run(text, expected):
    assert main.run(text) == expected
