import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (('1'), """Give me an integer number:""", 1),
    (
        ('dos', '2'),
        """Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:""",
        2,
    ),
    (
        ('tres', 'three', '3'),
        """Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:""",
        3,
    ),
    (
        ('cuatro', 'four', 'vier', '4'),
        """Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:""",
        4,
    ),
    (
        ('cinco', 'five', 'fünf', 'cinque', '5'),
        """Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:
Not a valid integer. Try it again!
Give me an integer number:""",
        5,
    ),
]


@pytest.mark.dependency()
def test_func_exists():
    assert getattr(main, 'getint', None), 'La función principal debe llamarse getint'


@pytest.mark.parametrize('inputs, expected_stdout, expected_return', testdata)
@pytest.mark.dependency(depends=['test_func_exists'])
def test_expected(inputs, expected_stdout, expected_return, monkeypatch, capsys):
    def gen_input():
        yield from inputs

    test_inputs = gen_input()

    def monkey_input(msg: str) -> str:
        print(msg.strip())
        return next(test_inputs)

    monkeypatch.setattr('builtins.input', monkey_input)
    assert main.getint() == expected_return
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_stdout
