import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (0, 1),
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (5, 120),
    (6, 720),
    (7, 5040),
    (8, 40_320),
    (9, 362_880),
    (10, 3_628_800),
    (-1, None),
]


@pytest.mark.dependency()
def test_func_exists():
    assert getattr(main, 'factorial', None), 'La función principal debe llamarse factorial'


@pytest.mark.parametrize('n, expected', testdata)
@pytest.mark.dependency(depends=['test_func_exists'])
def test_expected(n, expected):
    assert main.factorial(n) == expected
