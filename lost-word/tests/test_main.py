import os

import pytest

if os.path.exists('solution.py'):
    import solution as main
else:
    import main  # type:ignore

testdata = [
    (
        'This is a beautiful night on the Atlantic',
        'beautiful',
        'terrible',
        'This is a terrible night on the Atlantic',
    ),
    (
        'Tomorrow will be a wonderful day in the beach',
        'wonderful',
        'great',
        'Tomorrow will be a great day in the beach',
    ),
    ('Keep calm and write Python', 'write', 'enjoy', 'Keep calm and enjoy Python'),
]


@pytest.mark.parametrize('text, target_word, replace_word, expected', testdata)
def test_run(text, target_word, replace_word, expected):
    assert main.run(text, target_word, replace_word) == expected
