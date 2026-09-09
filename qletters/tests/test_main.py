import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (
        'AbCdeFGhIjKlmNOPqrSTuVwXyZaBcD',
        [
            'A',
            'C',
            'F',
            'G',
            'I',
            'K',
            'N',
            'O',
            'P',
            'S',
            'T',
            'V',
            'X',
            'Z',
            'B',
            'D',
            'b',
            'd',
            'e',
            'h',
            'j',
            'l',
            'm',
            'q',
            'r',
            'u',
            'w',
            'y',
            'a',
            'c',
        ],
    ),
    ('aBc DeFGhIj', ['D', 'F', 'G', 'I', 'e', 'h', 'j']),
    ('TRzxyABE pRYSumnW', ['R', 'Y', 'S', 'W', 'p', 'u', 'm', 'n']),
    ('xyz', ['x', 'y', 'z']),
    ('xyz', ['x', 'y', 'z']),
    ('xyz ', []),
    ('XYZ ', []),
    ('', []),
    (' ', []),
]


@pytest.mark.parametrize('letters, expected', testdata)
def test_run(letters, expected):
    assert main.run(letters) == expected
