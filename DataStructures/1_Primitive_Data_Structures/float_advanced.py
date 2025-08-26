"""
Advanced float utilities: ULPs, nextafter, compensated sums, stable formulas, NaN-safe operations.
Covers subtle issues in floating-point arithmetic and numerical stability.
"""
from __future__ import annotations
import math
from typing import Iterable, Tuple, List


# ---- ULP & neighbors ----
def ulp(x: float) -> float:
    """Return the Unit in the Last Place (ULP) of x.
    ULP = spacing between x and the next representable float.
    Shows machine precision around a given number.
    """
    return math.ulp(x)


def neighbors(x: float) -> Tuple[float, float]:
    """Return the floating-point neighbors of x:
    (previous representable float, next representable float).
    Uses math.nextafter for exact neighbors.
    """
    return (math.nextafter(x, -math.inf), math.nextafter(x, math.inf))


# ---- Summation strategies ----
def kahan_sum(xs: Iterable[float]) -> float:
    """Compensated summation (Kahan algorithm).
    Reduces floating-point error when adding many numbers.
    Tracks small errors in variable `c` and corrects them.
    """
    total = 0.0
    c = 0.0
    for x in xs:
        y = x - c        # correct small error
        t = total + y
        c = (t - total) - y  # recover lost low-order bits
        total = t
    return total


def neumaier_sum(xs: Iterable[float]) -> float:
    """Improved compensated summation (Neumaier’s algorithm).
    Handles cases where new number is larger than the running total.
    """
    it = iter(xs)
    try:
        total = next(it)
    except StopIteration:
        return 0.0
    c = 0.0
    for x in it:
        t = total + x
        if abs(total) >= abs(x):
            c += (total - t) + x
        else:
            c += (x - t) + total
        total = t
    return total + c


def pairwise_sum(xs: List[float]) -> float:
    """Pairwise summation: recursively split list and sum halves.
    Improves accuracy by reducing error growth (O(n log n) instead of O(n)).
    Requires random access (list).
    """
    n = len(xs)
    if n == 0:
        return 0.0
    if n == 1:
        return xs[0]
    m = n // 2
    return pairwise_sum(xs[:m]) + pairwise_sum(xs[m:])


# ---- Stable formulas ----
def hypot_stable(x: float, y: float) -> float:
    """Stable computation of sqrt(x^2 + y^2).
    math.hypot avoids overflow/underflow compared to naive formula.
    """
    return math.hypot(x, y)


def quadratic_roots_stable(a: float, b: float, c: float) -> Tuple[complex, complex]:
    """
    Stable quadratic root formula that avoids catastrophic cancellation.
    Returns two roots (possibly complex).
    Method: compute root using numerically stable rearrangement of formula.
    """
    if a == 0:
        raise ValueError("a must be nonzero")
    disc = b * b - 4 * a * c  # discriminant
    if disc >= 0:
        # Real roots
        s = math.sqrt(disc)
        # Avoid cancellation: choose sign of sqrt(disc) to match b
        q = -0.5 * (b + math.copysign(s, b))
        r1 = q / a
        r2 = c / q if q != 0 else (-b - s) / (2 * a)
        return (r1, r2)
    else:
        # Complex roots
        s = math.sqrt(-disc)
        real = -b / (2 * a)
        imag = s / (2 * abs(a))
        return (complex(real, imag), complex(real, -imag))


def logsumexp(values: Iterable[float]) -> float:
    """Compute log(sum(exp(x_i))) in a numerically stable way.
    Trick: subtract max to avoid overflow in exp.
    Used in statistics and machine learning.
    """
    vals = list(values)
    if not vals:
        return -math.inf
    m = max(vals)
    if math.isinf(m):
        return m
    s = sum(math.exp(v - m) for v in vals)
    return m + math.log(s)


# ---- NaN/Inf safe helpers ----
def safe_min(xs: Iterable[float]) -> float:
    """Return minimum value while ignoring NaNs.
    If all values are NaN, return NaN.
    Useful when dealing with datasets containing invalid values.
    """
    best = None
    for x in xs:
        if math.isnan(x):
            continue
        best = x if best is None or x < best else best
    return float("nan") if best is None else best


def safe_sort(xs: Iterable[float]) -> list[float]:
    """Sort numbers safely:
    - Places NaNs at the end.
    - Preserves ordering between -0.0 and +0.0 (negative zero first).
    - Keeps ±infinity in correct numeric order.
    """
    def key(x: float):
        if math.isnan(x):
            return (2, 0.0)  # NaNs last
        # Grouping:
        # (0) finite numbers, (1) infinities, (2) NaNs
        # Secondary key ensures -0.0 comes before +0.0
        return (0 if math.isfinite(x) else 1,
                (x, 1 if math.copysign(1.0, x) > 0 else 0))
    return sorted(xs, key=key)


# ---- Demo ----
if __name__ == "__main__":
    x = 1.0
    print("ulp(1.0):", ulp(x), "neighbors:", neighbors(x))

    # Summation accuracy comparison
    vals = [1e16, 1.0, -1e16]  # naive sum loses the '1.0'
    print("sum:", sum(vals),
          "kahan:", kahan_sum(vals),
          "neumaier:", neumaier_sum(vals))
    print("pairwise:", pairwise_sum(vals))

    # Stable formulas
    print("hypot_stable(3,4):", hypot_stable(3.0, 4.0))         # 5.0
    print("quad roots (1, -3, 2):", quadratic_roots_stable(1, -3, 2))  # (1.0, 2.0)

    # Robust log-sum-exp
    print("logsumexp([1000, 1001]):", logsumexp([1000.0, 1001.0]))

    # Safe sorting
    print("safe_sort:",
          safe_sort([float('nan'), 3.0, -0.0, 0.0, float('inf'), -float('inf')]))
