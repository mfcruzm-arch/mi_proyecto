import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (['uno', 'dos', 'tres'], ['u', 'n', 'o', 'd', 'o', 's', 't', 'r', 'e', 's']),
    (['abc', 'abc', 'abc'], ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']),
    (['XZ', 'VW'], ['X', 'Z', 'V', 'W']),
    (['alone'], ['a', 'l', 'o', 'n', 'e']),
    (['', '', ''], []),
]


@pytest.mark.parametrize('texts, expected', testdata)
def test_run(texts, expected):
    assert main.run(texts) == expected
