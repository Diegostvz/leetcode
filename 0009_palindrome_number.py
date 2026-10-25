"""
LeetCode 9 - Palindrome Number (Easy)
https://leetcode.com/problems/palindrome-number/

Problem:
    Given an integer x, return True if x is a palindrome (reads the same
    forwards and backwards), and False otherwise.
    Negative numbers are never palindromes: "-121" reversed is "121-".

Approach 1 - Two pointers over the string (my solution):
    Reject negatives upfront, then convert x to a string and compare characters
    from both ends, moving inwards. Return False on the first mismatch (early exit).
    Negatives are handled implicitly: '-' never matches the last digit.
    Time: O(d) | Space: O(d), with d = number of digits

Approach 2 - Built-in slicing (Claude suggested simplification):
    Reject negatives upfront, then compare the string with its reverse.
    Same complexity and no early exit, but faster in practice: slicing
    and string comparison run in C inside CPython, while the two-pointer
    loop is executed instruction by instruction by the interpreter.
    For inputs of at most ~10 digits, the early exit cannot compensate
    for the interpreter overhead.
    Time: O(d) | Space: O(d)

Lessons learned:
    - Read the examples carefully: the sign is part of the representation.
    - In Python, built-ins usually beat hand-written loops with the same
      Big-O. Two pointers still shows algorithmic understanding in interviews.
"""


class SolutionV1:
    """My solution: two pointers with early exit."""

    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        str_x = str(x)
        left = 0
        right = len(str_x) - 1

        while left <= right:
            if str_x[left] != str_x[right]:
                return False
            left += 1
            right -= 1

        return True


class Solution:
    """Suggested simplification: leverage CPython's C-level slicing."""

    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        s = str(x)
        return s == s[::-1]


if __name__ == "__main__":
    tests = [
        (121, True),
        (-121, False),
        (10, False),
        (0, True),
        (1221, True),
        (12321, True),
        (123, False),
    ]
    for solver in (SolutionV1(), Solution()):
        for inp, expected in tests:
            assert solver.isPalindrome(inp) == expected, (type(solver).__name__, inp)
    print("OK")
