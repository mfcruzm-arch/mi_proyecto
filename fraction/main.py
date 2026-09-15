from __future__ import annotations


class Fraction:
	def __init__(self, num: int, den: int):
		self.num = num
		self.den = den

	def __str__(self) -> str:
		return f'{self.num}/{self.den}'

	def simplify(self) -> None:
		divisor = self._gcd(self.num, self.den)
		self.num //= divisor
		self.den //= divisor

	def __add__(self, other: Fraction) -> Fraction | None:
		if not isinstance(other, Fraction):
			return None
		result = Fraction(
			self.num * other.den + other.num * self.den,
			self.den * other.den,
		)
		result.simplify()
		return result

	def __sub__(self, other: Fraction) -> Fraction | None:
		if not isinstance(other, Fraction):
			return None
		result = Fraction(
			self.num * other.den - other.num * self.den,
			self.den * other.den,
		)
		result.simplify()
		return result

	def __mul__(self, other: Fraction) -> Fraction | None:
		if not isinstance(other, Fraction):
			return None
		result = Fraction(self.num * other.num, self.den * other.den)
		result.simplify()
		return result

	def __truediv__(self, other: Fraction) -> Fraction | None:
		if not isinstance(other, Fraction):
			return None
		result = Fraction(self.num * other.den, self.den * other.num)
		result.simplify()
		return result

	@staticmethod
	def _gcd(first: int, second: int) -> int:
		first = abs(first)
		second = abs(second)
		while second:
			first, second = second, first % second
		return first

