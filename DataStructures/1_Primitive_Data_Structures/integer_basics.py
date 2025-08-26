"""
Integer basics: arithmetic, base conversions, bit operations, and small utilities.
Run this file to see demo output.
"""
from __future__ import annotations

'''
The line from __future__ import annotations is used in Python to change the way type hints are handled. 
Normally, when you write type hints, Python tries to evaluate them immediately into actual objects. 
With this future import, however, all annotations are stored as plain strings instead of being executed right away. 
This has a few important advantages. First, it allows you to use forward references, meaning you can refer to classes 
or types that are defined later in the file without running into errors. This is especially helpful when dealing 
with recursive data structures or circular imports. Second, it improves performance slightly because type hints 
don’t need to be evaluated during runtime. Finally, it makes your code more consistent and forward-compatible with 
newer versions of Python, since deferred evaluation of annotations has become the standard in recent releases. 
In your current code, you don’t strictly need it, but including it is generally considered a good practice for larger 
projects or libraries where complex type hints are used.
'''


# Check if a number is even
def is_even(n: int) -> bool:
     return (n & 1) == 0
    # A number is even if its last binary bit is 0.
    # Bitwise AND with 1 extracts the last bit:
    # - If n is even, (n & 1) = 0
    # - If n is odd,  (n & 1) = 1
   


# Convert a number into multiple bases
def to_bases(n: int) -> dict[str, str]:
    return {"bin": bin(n), "oct": oct(n), "dec": str(n), "hex": hex(n)}
    # bin() → binary string, e.g. 42 -> '0b101010'
    # oct() → octal string,  e.g. 42 -> '0o52'
    # str() → decimal string, e.g. 42 -> '42'
    # hex() → hexadecimal string, e.g. 42 -> '0x2a'


# Count the number of 1 bits in the binary representation of n
def count_set_bits(n: int) -> int:
    # Brian Kernighan’s algorithm:
    # Repeatedly remove the lowest set bit until n becomes 0.
    # Example: n = 0b101101 (45)
    # 1st iteration: 0b101101 & 0b101100 -> 0b101100
    # 2nd iteration: 0b101100 & 0b101011 -> 0b101000
    # 3rd iteration: 0b101000 & 0b100111 -> 0b100000
    # 4th iteration: 0b100000 & 0b011111 -> 0
    # Count = 4 set bits
    c = 0
    while n:
        n &= n - 1
        c += 1
    return c


# Compute the greatest common divisor (GCD) of two numbers
def gcd(a: int, b: int) -> int:
    # Euclidean algorithm:
    # Keep replacing (a, b) with (b, a % b) until b == 0
    # At that point, a is the GCD
    while b:
        a, b = b, a % b
    return abs(a)  # GCD should always be non-negative


# Compute the least common multiple (LCM) of two numbers
def lcm(a: int, b: int) -> int:
    # Formula: lcm(a, b) = abs(a * b) // gcd(a, b)
    # Rewritten to avoid overflow: (a // gcd(a, b)) * b
    # Special case: if either number is 0 → LCM is 0
    return 0 if a == 0 or b == 0 else abs(a // gcd(a, b) * b)


if __name__ == "__main__":
    # Demo values
    n = 42
    print("is_even(42):", is_even(n))  # True
    print("to_bases(42):", to_bases(n))  # {'bin': '0b101010', 'oct': '0o52', 'dec': '42', 'hex': '0x2a'}
    print("count_set_bits(0b101101):", count_set_bits(0b101101))  # 4
    print("gcd(54, 24):", gcd(54, 24))  # 6
    print("lcm(12, 18):", lcm(12, 18))  # 36
