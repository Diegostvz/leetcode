"""
0005. Longest Palindromic Substring — Medium
https://leetcode.com/problems/longest-palindromic-substring/
Pattern: expand around center
Complexity: O(n^2) time, O(1) space
Notes:
- Every palindrome is symmetric around a center: either a single character
  (odd length) or the gap between two characters (even length).
  That gives 2n - 1 centers; expanding from each one costs O(n).
- expand() stops one step too far on each side, hence the start is left + 1
  and the length is right - left - 1.
- Manacher's algorithm solves it in O(n), but it is rarely expected in
  interviews; expand-around-center is the standard answer.
"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        best_start, best_len = 0, 0

        def expand(left: int, right: int) -> tuple[int, int]:
            """Expand from (left, right) and return (start, length) of the palindrome."""
            while left >= 0 and right < n and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - left - 1

        for center in range(n):
            # Center on a character (odd length) and between two characters (even)
            for left, right in ((center, center), (center, center + 1)):
                start, length = expand(left, right)
                if length > best_len:
                    best_start, best_len = start, length

        return s[best_start : best_start + best_len]


if __name__ == "__main__":
    sol = Solution()
    assert sol.longestPalindrome("babad") in ("bab", "aba")
    assert sol.longestPalindrome("cbbd") == "bb"
    assert sol.longestPalindrome("a") == "a"
    assert sol.longestPalindrome("forgeeksskeegfor") == "geeksskeeg"
    print("OK")
