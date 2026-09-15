import os

if os.path.exists('solution.py'):
    from solution import Fraction
else:
    from main import Fraction  # type:ignore


def test_fraction_is_built_right(fraction1: Fraction, fraction2: Fraction):
    assert fraction1.num == 25
    assert fraction1.den == 30
    assert fraction2.num == 40
    assert fraction2.den == 45


def test_fraction_str_is_correct(fraction1: Fraction, fraction2: Fraction):
    assert str(fraction1) == '25/30'
    assert str(fraction2) == '40/45'


def test_fraction_sum_is_right(fraction1: Fraction, fraction2: Fraction):
    result = fraction1 + fraction2
    assert result.num == 31
    assert result.den == 18


def test_fraction_sub_is_right(fraction1: Fraction, fraction2: Fraction):
    result = fraction1 - fraction2
    assert result.num == -1
    assert result.den == 18


def test_fraction_mul_is_right(fraction1: Fraction, fraction2: Fraction):
    result = fraction1 * fraction2
    assert result.num == 20
    assert result.den == 27


def test_fraction_div_is_right(fraction1: Fraction, fraction2: Fraction):
    result = fraction1 / fraction2
    assert result.num == 15
    assert result.den == 16


def test_fraction_add_wrong_type(fraction1: Fraction):
    result = fraction1 + 5
    assert result is None


def test_fraction_sub_wrong_type(fraction1: Fraction):
    result = fraction1 - 5  # type:ignore
    assert result is None


def test_fraction_mul_wrong_type(fraction1: Fraction):
    result = fraction1 * 5  # type:ignore
    assert result is None


def test_fraction_div_wrong_type(fraction1: Fraction):
    result = fraction1 / 5  # type:ignore
    assert result is None


def test_fraction_is_correctly_simplified(fraction1: Fraction, fraction2: Fraction):
    fraction1.simplify()
    fraction2.simplify()
    assert fraction1.num == 5
    assert fraction1.den == 6
    assert fraction2.num == 8
    assert fraction2.den == 9
