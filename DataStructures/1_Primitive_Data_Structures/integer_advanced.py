"""
Advanced integers: bit hacks, bitset tricks, modular arithmetic, primality testing, and sieve.
This file demonstrates useful low-level number theory and bit manipulation utilities.
"""
from __future__ import annotations
from typing import Iterable, Tuple, List

'''
The line from typing import Iterable, Tuple, List is used to bring in type-hinting tools from Python’s typing module, 
which helps make the code clearer and easier to check. The Iterable type indicates that a parameter can be any object 
you can loop over, such as a list, set, or generator. In your code, it is used for the indices parameter in 
bitset_from_indices, meaning the function can accept any iterable of integers. The Tuple type is used to represent a 
fixed-length sequence with specific types; for example, the egcd function is annotated to return a tuple of three 
integers (g, x, y). The List type specifies a standard Python list containing elements of a particular type; in your 
code, the sieve function returns a list of integers representing prime numbers. These annotations don’t affect how the 
program runs but improve readability, make the expected inputs and outputs explicit, and allow tools like IDEs and 
static type checkers (e.g., mypy) to catch type-related errors before runtime.
'''
import random


# ---- Bit hacks ----
def lowbit(x: int) -> int:
    """Return the lowest set bit of x as a power of two.
    Example: lowbit(52=0b110100) → 0b100 = 4
    Trick: x & -x isolates the rightmost 1 in binary.
    """
    return x & -x


def msb_index(x: int) -> int:
    """Return the 0-based index of the most significant set bit.
    For example, msb_index(1024=2^10) → 10.
    Uses x.bit_length()-1 (bit_length = position of top bit + 1).
    """
    if x <= 0:
        raise ValueError("x must be positive")
    return x.bit_length() - 1


def mask_low(nbits: int) -> int:
    """Return a mask with the lowest nbits set to 1.
    Example: mask_low(5) → 0b11111 = 31
    Uses (1 << nbits) - 1 trick.
    """
    return (1 << nbits) - 1 if nbits > 0 else 0


# ---- Bitset using a single integer ----
def bitset_from_indices(indices: Iterable[int]) -> int:
    """Build a bitset from a collection of indices.
    Example: indices [0,2,5] → bitset 0b100101
    Each index i sets the ith bit of an integer.
    """
    bs = 0
    for i in indices:
        if i < 0:
            raise ValueError("indices must be non-negative")
        bs |= 1 << i
    return bs


def bitset_add(bs: int, i: int) -> int:
    """Add element i to bitset bs (set the ith bit)."""
    return bs | (1 << i)


def bitset_remove(bs: int, i: int) -> int:
    """Remove element i from bitset bs (clear the ith bit)."""
    return bs & ~(1 << i)


def bitset_contains(bs: int, i: int) -> bool:
    """Check if element i is in bitset bs (if ith bit is set)."""
    return ((bs >> i) & 1) == 1


def bitset_iter(bs: int):
    """Yield indices of set bits in bs.
    Uses Kernighan’s loop: repeatedly removes the lowest set bit.
    Efficient way to enumerate bits in a bitset.
    """
    while bs:
        lb = bs & -bs  # isolate lowest set bit
        yield lb.bit_length() - 1
        bs ^= lb       # clear that bit


# ---- Number theory ----
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclidean algorithm.
    Returns (g, x, y) such that: a*x + b*y = g = gcd(a, b).
    Useful for modular inverses.
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def modinv(a: int, m: int) -> int:
    """Modular inverse of a modulo m.
    Returns x such that (a*x) % m = 1, if it exists.
    Uses Extended Euclidean Algorithm.
    Raises ValueError if inverse does not exist.
    """
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("inverse does not exist")
    return x % m


def modexp(base: int, exp: int, mod: int) -> int:
    """Modular exponentiation: (base^exp) % mod.
    Uses Python’s built-in pow with 3 arguments, which is very efficient.
    """
    return pow(base, exp, mod)


# ---- Miller–Rabin primality test ----
# Deterministic bases for testing < 2^64
_DET_BASES_64 = [2, 3, 5, 7, 11, 13, 17]


def _decompose(n: int):
    """Write n-1 as d * 2^s with d odd.
    Example: n=21 → 20=5*2^2 → d=5, s=2.
    """
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return d, s


def _check_witness(a: int, s: int, d: int, n: int) -> bool:
    """Check if 'a' is a Miller-Rabin witness for compositeness."""
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False


def is_probable_prime(n: int, rounds: int = 8) -> bool:
    """Miller–Rabin primality test.
    Returns True if n is probably prime, False if composite.
    For n < 2^64, deterministic using fixed bases.
    For larger n, uses 'rounds' random bases.
    """
    if n < 2:
        return False
    # Trial division by small primes
    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False
    # Write n-1 = d * 2^s
    d, s = _decompose(n)
    # Use deterministic bases if n < 2^64, else random bases
    bases = _DET_BASES_64 if n < (1 << 64) else [random.randrange(2, n - 2) for _ in range(rounds)]
    return all(_check_witness(a, s, d, n) for a in bases)


# ---- Sieve of Eratosthenes using bitset (odds only) ----
def sieve(limit: int) -> List[int]:
    """Return all primes <= limit using sieve of Eratosthenes.
    Optimized by storing only odd numbers in a bitset (half memory).
    """
    if limit < 2:
        return []
    size = limit // 2  # we only track odd numbers
    composite = 0
    import math

    r = int(limit ** 0.5)
    for i in range(3, r + 1, 2):
        idx = i // 2
        if ((composite >> idx) & 1) == 0:  # if i is prime
            start = (i * i) // 2  # start marking from i^2
            step = i              # mark every i steps
            for j in range(start, size, step):
                composite |= 1 << j
    # Collect primes: 2 plus all unmarked odds
    primes = [2] + [2 * i + 1 for i in range(1, size) if ((composite >> i) & 1) == 0 and 2 * i + 1 <= limit]
    return primes


# ---- Demo ----
if __name__ == "__main__":
    print("lowbit(52):", lowbit(52))                        # 4
    print("msb_index(1024):", msb_index(1024))              # 10
    bs = bitset_from_indices([0, 2, 5])
    print("bitset:", bin(bs), "contains 2?", bitset_contains(bs, 2))
    print("modinv(3, 11):", modinv(3, 11))                  # 4, since 3*4 ≡ 1 (mod 11)
    print("is_probable_prime(2**61-1):", is_probable_prime((1 << 61) - 1))
    print("sieve(50):", sieve(50))                          # [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
