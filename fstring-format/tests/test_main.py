import os

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore


def test_result(capsys):
    main.run(2.71828)
    captured = capsys.readouterr()
    assert (
        captured.out
        == """
2.718
2.718280
    2.72
2.718280e+00
00002.7183
            2.71828
""".lstrip()
    )
