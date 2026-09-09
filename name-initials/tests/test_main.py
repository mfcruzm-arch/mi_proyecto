import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ('Delgado Quintero, sergio', 'S.D.Q.'),
    ('sánchez, María', 'M.S.'),
    ('Prado López, Ana Belén', 'A.P.L.'),
]


@pytest.mark.parametrize('fullname, expected', testdata)
def test_run(fullname, expected):
    assert main.run(fullname) == expected
