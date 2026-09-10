import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main

testdata = [
    (3, -4, 25),
    (-5, -7, 74),
    (-2, 8, 68),
]


@pytest.mark.dependency()
def test_func_exists():
    assert getattr(main, 'f', None), 'La función principal debe llamarse f'


@pytest.mark.parametrize('x, y, expected', testdata)
@pytest.mark.dependency(depends=['test_func_exists'])
def test_expected(x, y, expected):
    assert main.f(x, y) == expected
