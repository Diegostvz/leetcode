"""
LeetCode 8 - String to Integer (atoi) (Medium)
https://leetcode.com/problems/string-to-integer-atoi/

Problem:
    Convert a string to a signed 32-bit integer following these steps:
      1. Skip leading whitespace.
      2. Read an optional '+' or '-' sign.
      3. Read digits until the first non-digit character (or end of string).
      4. Apply the sign and clamp the result to [-2^31, 2^31 - 1].
    If no digits are read, return 0.

Approach 1 - Positional weights (my first accepted solution):
    Weight each digit by 10^(len - 1 - idx) using the total length of the
    remaining string, and rescale with an integer division when the first
    non-digit appears. Clamp at the end.
    Time: O(n^2) worst case | Space: O(n)
    Limitation: the weights depend on the full string length, so even a
    single digit followed by many letters produces huge intermediate
    integers (e.g. "1" + "a"*10000 computes 10^10000). Big-int arithmetic
    in Python is not O(1), so cost grows with n on every iteration.

Approach 2 - Left-to-right accumulation with early clamping (optimal):
    Build the number with sol = 10*sol + digit, reading left to right, so
    the string length is irrelevant. As soon as the magnitude exceeds
    INT_MAX it can never come back into range, so return the clamped
    bound immediately. Since |INT_MIN| = INT_MAX + 1, any magnitude above
    INT_MAX also clamps correctly to INT_MIN when the sign is negative.
    Intermediate values never exceed ~11 digits, so each step is O(1).
    Time: O(n) | Space: O(n) for the stripped/sliced string, O(1) extra

Lessons learned:
    - str methods (strip, replace...) return new strings: always reassign.
    - Accumulating left to right avoids needing to know the length upfront.
    - LeetCode runtime percentiles are noisy on small inputs; rely on
      complexity analysis and benchmark with large inputs.
"""

INT_MIN, INT_MAX = -(2**31), 2**31 - 1


class SolutionV1:
    """First accepted solution (positional weights)."""

    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        sol = 0
        sign = 1
        if s == "":
            return 0
        elif s[0] == "-":
            sign = -1
            s = s[1:]
        elif s[0] == "+":
            s = s[1:]

        n_letters = len(s)
        for idx, elem in enumerate(s):
            if elem.isnumeric():
                sol += int(elem) * 10 ** (n_letters - 1 - idx)
            else:
                # Rescale: digits were weighted as if the string were all digits
                signed_sol = sign * sol // (10 ** (n_letters - idx))
                return (
                    max(signed_sol, INT_MIN) if sign == -1 else min(signed_sol, INT_MAX)
                )

        signed_sol = sign * sol
        return max(signed_sol, INT_MIN) if sign == -1 else min(signed_sol, INT_MAX)


class Solution:
    """Optimal solution: left-to-right accumulation with early clamping."""

    def myAtoi(self, s: str) -> int:
        # 1. Skip leading whitespace
        s = s.lstrip()
        if not s:
            return 0

        # 2. Optional sign
        sign = 1
        if s[0] in "+-":
            sign = -1 if s[0] == "-" else 1
            s = s[1:]

        # 3. Read digits, clamping as soon as the magnitude overflows
        sol = 0
        for ch in s:
            if not ch.isdigit():
                break
            sol = 10 * sol + int(ch)
            if sol > INT_MAX:
                return INT_MAX if sign == 1 else INT_MIN

        # 4. Apply sign (already guaranteed to be in range)
        return sign * sol


if __name__ == "__main__":
    tests = [
        ("4193 with words", 4193),
        ("42", 42),
        ("    -042", -42),
        ("1337c0d3", 1337),
        ("0-1", 0),
        ("words and 987", 0),
        ("", 0),
        ("     ", 0),
        ("+-12", 0),
        ("1 2", 1),
        ("-91283472332", INT_MIN),
        ("91283472332", INT_MAX),
        ("-2147483648", INT_MIN),
        ("-2147483649", INT_MIN),
        ("2147483647", INT_MAX),
    ]
    for solver in (SolutionV1(), Solution()):
        for inp, expected in tests:
            assert solver.myAtoi(inp) == expected, (type(solver).__name__, inp)

    # Large input: only the optimal version handles this efficiently
    assert Solution().myAtoi("9" * 100000) == INT_MAX
    print("OK")
