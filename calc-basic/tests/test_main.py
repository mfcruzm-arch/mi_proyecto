import os

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore


def test_result(monkeypatch, capsys):
    def monkey_input(foo):
        return '3'

    monkeypatch.setattr('builtins.input', monkey_input)
    main.run()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """
3+3=6
3-3=0
3*3=9
3/3=1.0
""".lstrip()
    )
