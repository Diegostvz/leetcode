"""
LeetCode 29 - Divide Two Integers (Medium)

Problem: Given two integers dividend and divisor, divide them WITHOUT using multiplication,
division or the mod operator. The result truncates toward zero (7 / -3 = -2). Only 32-bit
signed integers are allowed: if the quotient is above 2^31 - 1, return 2^31 - 1; if it is
below -2^31, return -2^31.
(-2^31 <= dividend, divisor <= 2^31 - 1, divisor != 0)

Common steps (both approaches):
    - Work with absolute values; the sign is negative iff exactly one input is negative:
      (dividend < 0) != (divisor < 0). Negating (-q) and abs are allowed.
    - Clamp the result to [-2^31, 2^31 - 1]. The only overflow is -2^31 / -1 = 2^31.

Approach 1 - Repeated subtraction (divideSubtraction):
    Key idea: by definition, the quotient is how many times the divisor can be subtracted from
    the dividend: subtract it one by one and count.

    Complexity (D = |dividend|, d = |divisor|):
        Time:  O(D / d) -> one iteration per unit of the quotient. Worst case d = 1:
               2^31 iterations -> Time Limit Exceeded on LeetCode.
        Space: O(1) -> a few variables.

Approach 2 - Subtract the biggest multiple, found by doubling (divide):
    Key idea: instead of subtracting d once per iteration, in each round subtract the biggest
    multiple d * 2^j that still fits in the remainder. It is found by doubling (chunk + chunk)
    both the chunk and the count of how many times it contains d. Each round adds one binary
    digit of the quotient.

        100 / 3:  3 -> 6 -> 12 -> 24 -> 48 -> 96  (192 no longer fits)
                  remainder = 100 - 96 = 4, q += 32
                  remainder 4: 3 fits, 6 does not  -> remainder = 1, q += 1
                  1 < 3 -> stop, q = 33 (= 32 + 1, binary 100001)

    Complexity (D = |dividend|, d = |divisor|):
        Time:  O(log^2(D / d)) -> at most log2(D / d) rounds (each one removes at least half
               of the remainder), and up to log2(D / d) doublings per round.
               With D = 2^31: about 31 * 31 ~ 1000 operations instead of 2 * 10^9.
        Space: O(1) -> a few variables.

    Note:
        - Every round must start again from the ORIGINAL divisor: chunk grows only inside the
          round. chunk is removed from the remainder; multiple is added to the quotient.
        - x + x (or x << 1) doubles without multiplying.
        - Can be made O(log(D / d)): precompute the doublings once and walk them back from
          the largest (this is exactly binary long division).
        - In Python integers do not overflow, so |-2^31| = 2^31 is safe; in languages with
          32-bit ints, the usual trick is to work with negative values instead.
"""

INT_MAX = 2**31 - 1
INT_MIN = -(2**31)


class Solution:
    def divideSubtraction(self, dividend: int, divisor: int) -> int:
        """Subtract the divisor one by one and count the subtractions."""
        remainder = abs(dividend)
        abs_divisor = abs(divisor)

        q = 0
        while remainder >= abs_divisor:
            remainder -= abs_divisor
            q += 1

        if (dividend < 0) != (divisor < 0):  # exactly one negative
            q = -q
        return max(INT_MIN, min(q, INT_MAX))  # clamp to 32-bit range

    def divide(self, dividend: int, divisor: int) -> int:
        """Each round, subtract the biggest doubling of the divisor that fits."""
        remainder = abs(dividend)
        abs_divisor = abs(divisor)

        q = 0
        while remainder >= abs_divisor:  # one round per binary digit of q
            chunk = abs_divisor  # every round starts from the original divisor
            multiple = 1
            while chunk + chunk <= remainder:  # double while it still fits
                chunk += chunk
                multiple += multiple
            remainder -= chunk  # remove the biggest multiple that fits
            q += multiple  # it contained the divisor `multiple` times

        if (dividend < 0) != (divisor < 0):  # exactly one negative
            q = -q
        return max(INT_MIN, min(q, INT_MAX))  # clamp to 32-bit range


if __name__ == "__main__":
    sol = Solution()

    small_cases = [
        (10, 3, 3),
        (7, -3, -2),  # truncates toward zero, not -3
        (-10, 3, -3),
        (-7, -3, 2),
        (0, 3, 0),
        (1, 1, 1),
        (3, 5, 0),  # |dividend| < |divisor|
        (100, 3, 33),
    ]
    big_cases = [
        (INT_MAX, 1, INT_MAX),  # max: too slow with one-by-one subtraction
        (INT_MIN, 1, INT_MIN),  # min
        (INT_MIN, -1, INT_MAX),  # overflow: 2^31 does not fit -> clamp
        (INT_MIN, 2, -(2**30)),
        (INT_MAX, 2, 2**30 - 1),
        (INT_MIN, INT_MIN, 1),
        (INT_MAX, INT_MIN, 0),
    ]

    # Approach 1 only on small inputs: the big ones take minutes (that is the point)
    for dividend, divisor, expected in small_cases:
        result = sol.divideSubtraction(dividend, divisor)
        assert result == expected, ("divideSubtraction", dividend, divisor, result)
    print("divideSubtraction: OK (small cases only)")

    for dividend, divisor, expected in small_cases + big_cases:
        result = sol.divide(dividend, divisor)
        assert result == expected, ("divide", dividend, divisor, result)

    # Cross-check against Python's own division, truncated toward zero
    import random

    for _ in range(10_000):
        a = random.randint(INT_MIN, INT_MAX)
        b = (
            random.choice(
                [random.randint(-1000, 1000), random.randint(INT_MIN, INT_MAX)]
            )
            or 1
        )
        expected = max(
            INT_MIN, min(abs(a) // abs(b) * (-1 if (a < 0) != (b < 0) else 1), INT_MAX)
        )
        assert sol.divide(a, b) == expected, (a, b)
    print("divide: OK")
