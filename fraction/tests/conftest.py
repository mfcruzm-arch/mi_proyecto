import os

import pytest

if os.path.exists('solution.py'):
    from solution import Fraction
else:
    from main import Fraction  # type:ignore

# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def fraction1():
    return Fraction(25, 30)


@pytest.fixture
def fraction2():
    return Fraction(40, 45)
