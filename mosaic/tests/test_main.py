import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (
        3,
        """X U U
D X U
D D X""",
    ),
    (
        5,
        """X U U U U
D X U U U
D D X U U
D D D X U
D D D D X""",
    ),
    (
        7,
        """X U U U U U U
D X U U U U U
D D X U U U U
D D D X U U U
D D D D X U U
D D D D D X U
D D D D D D X""",
    ),
]


@pytest.mark.parametrize('size, expected', testdata)
def test_run(size, expected, capsys):
    main.run(size)
    captured = capsys.readouterr()
    for row, expected_row in zip(captured.out.strip().split('\n'), expected.split('\n')):
        assert row.strip() == expected_row.strip()
