import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ('Manuel', 'Eloisa', 'Manisa'),
    ('Camila', 'Daniel', 'Camiel'),
    ('Luciano', 'Valeria', 'Luceria'),
    ('Patricia', 'Zoe', 'Patroe'),
    ('Alejandro', 'Felipe', 'Alejipe'),
]


@pytest.mark.parametrize('word1, word2, expected', testdata)
def test_run(word1, word2, expected):
    assert main.run(word1, word2) == expected
