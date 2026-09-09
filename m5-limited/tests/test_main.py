import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (36, (5, 10, 15, 20, 25, 30, 35)),
    (12, (5, 10)),
    (25, (5, 10, 15, 20)),
    (4, tuple()),
]


@pytest.mark.parametrize('limit, expected', testdata)
def test_result(limit, expected, capsys):
    main.run(limit)
    captured = capsys.readouterr()
    assert captured.out == ''.join(f'{e}\n' for e in expected)
