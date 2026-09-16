import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    ('data/python.txt', 'desarrolladores'),
    ('data/java.txt', 'significativamente'),
    ('data/rust.txt', 'desreferenciación'),
]


@pytest.mark.parametrize('input_path, expected', testdata)
def test_run(input_path, expected):
    assert main.run(input_path) == expected
