import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (5, 523.3333333333334),
    (15.658, 16072.271158372905),
    (9.99, 4174.11922248),
]


@pytest.mark.parametrize('radius, expected', testdata)
def test_run(radius, expected):
    assert main.run(radius) == expected
