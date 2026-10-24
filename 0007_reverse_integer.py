"""
LeetCode 7 - Reverse Integer (Medium)
https://leetcode.com/problems/reverse-integer/

Problem:
    Given a signed 32-bit integer x, return x with its digits reversed.
    If reversing x causes the value to go outside the signed 32-bit
    range [-2^31, 2^31 - 1], return 0.
    Assume the environment does not allow storing 64-bit integers.

Approach 1 - Positional reconstruction (my first solution):
    Convert |x| to a string and rebuild the number by weighting the
    digit at index i with 10^i, which reverses the digit order.
    Re-apply the sign and check the 32-bit range at the end.
    Time: O(log|x|) | Space: O(log|x|)
    Limitation: builds the full reversed value before checking bounds,
    which relies on Python's arbitrary-precision integers.

Approach 2 - Digit pop/push with pre-overflow check (optimal):
    Pop the last digit with divmod and push it onto the result.
    Before each push, check that rev * 10 + digit cannot exceed INT_MAX,
    so the value never leaves the 32-bit range.
    Time: O(log|x|) | Space: O(1)
"""

INT_MIN, INT_MAX = -(2**31), 2**31 - 1


class SolutionV1:
    """First accepted solution (positional reconstruction)."""

    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        digits = str(abs(x))
        rev = sum(int(d) * 10**i for i, d in enumerate(digits))
        result = sign * rev
        return result if INT_MIN <= result <= INT_MAX else 0


class Solution:
    """Optimal solution: O(1) space, no intermediate overflow. Claude suggested the idea"""

    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x = abs(x)
        rev = 0
        while x:
            x, digit = divmod(x, 10)
            if rev > (INT_MAX - digit) // 10:  # rev*10 + digit > INT_MAX
                return 0
            rev = rev * 10 + digit
        return sign * rev


if __name__ == "__main__":
    sol = Solution()
    assert sol.reverse(0) == 0
    assert sol.reverse(123) == 321
    assert sol.reverse(-123) == -321
    assert sol.reverse(120) == 21
    print("OK")
