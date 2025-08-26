"""
Float basics: precision issues, safe comparisons, math helpers, and exact alternatives.
Demonstrates why floats can be tricky and how to use Decimal/Fraction for exact math.
"""
from __future__ import annotations
import math
from decimal import Decimal
from fractions import Fraction


# ---- Floating-point comparisons ----
def isclose(a: float, b: float, rel: float = 1e-9, abs_: float = 0.0) -> bool:
    """Return True if floats a and b are approximately equal.
    Uses relative tolerance (rel) and absolute tolerance (abs_).
    This avoids problems like 0.1 + 0.2 not being exactly 0.3.
    """
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)


# ---- Geometry helper ----
def triangle_area_heron(a: float, b: float, c: float) -> float:
    """Compute triangle area using Heron's formula:
       area = sqrt(s * (s-a) * (s-b) * (s-c)), where s = (a+b+c)/2
       Returns NaN if the sides do not form a valid triangle.
    """
    s = (a + b + c) / 2
    d = s * (s - a) * (s - b) * (s - c)
    return math.sqrt(d) if d >= 0 else float("nan")


# ---- Exact decimal arithmetic ----
def exact_decimal_sum(values: list[str]) -> Decimal:
    """Return exact sum of decimal strings using Decimal.
    Strings are used instead of floats to avoid binary rounding errors.
    Example: exact_decimal_sum(["19.99", "0.01", "5.00"]) = Decimal('25.00')
    """
    total = Decimal("0")
    for v in values:
        total += Decimal(v)
    return total


# ---- Exact rational arithmetic ----
def exact_fraction_average(fracs: list[tuple[int, int]]) -> Fraction:
    """Return the average of a list of fractions given as (numerator, denominator).
    Uses Fraction for exact rational math.
    Example: [(1,3), (1,6), (1,2)] → Fraction(7,18) ≈ 0.3888...
    """
    fs = [Fraction(n, d) for n, d in fracs]
    return sum(fs, Fraction(0, 1)) / len(fs)


# ---- Demo ----
if __name__ == "__main__":
    # Floating-point equality issue
    print("0.1 + 0.2 == 0.3 ?", 0.1 + 0.2 == 0.3)     # False, due to precision error
    print("isclose:", isclose(0.1 + 0.2, 0.3))        # True, with tolerance

    # Triangle area example
    print("heron(3,4,5):", triangle_area_heron(3, 4, 5))  # 6.0

    # Exact decimal example
    print("exact_decimal_sum:", exact_decimal_sum(["19.99", "0.01", "5.00"]))  # 25.00

    # Exact fraction average
    avg = exact_fraction_average([(1, 3), (1, 6), (1, 2)])
    print("fraction average:", avg, "≈", float(avg))     # 7/18 ≈ 0.3888...
