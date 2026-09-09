import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ('El camión chocó contra el árbol', 11),
    ('WELCOME HOME', 5),
    ('Órbita Laica', 6),
    ('Programar va de pensar, no de escribir', 12),
    ('Simple es mejor que complejo', 10),
]


@pytest.mark.parametrize('text, expected', testdata)
def test_run(text, expected):
    assert main.run(text) == expected
