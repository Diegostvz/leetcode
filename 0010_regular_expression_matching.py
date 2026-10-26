"""
LeetCode 10 - Regular Expression Matching (Hard)

Problem: given a string `s` and a pattern `p`, implement regular expression
matching with support for:
    '.'  -> matches any single character
    '*'  -> matches zero or more of the PRECEDING element in the pattern
The match must cover the entire input string, not just part of it.

Key idea:
    Read the pattern as "tokens": either `x` (a letter or '.') or `x*`.
    For an `x*` token we don't decide how many characters to consume up front;
    instead we try two options and accept whichever one works:
        1. Skip: ignore `x*` (use it zero times) -> advance 2 in p.
        2. Consume one: if s[i] matches x, advance 1 in s and stay at the
           same position in p (the '*' may keep consuming).

Optimization:
    The state of the problem is fully defined by the pair (i, j): position in
    s and position in p. Without memoization, many different paths recompute
    the same (i, j) -> exponential time. With memoization each pair is
    computed only once.

Complexity:
    Time:  O(len(s) * len(p))  -> number of possible states
    Space: O(len(s) * len(p))  -> cache + recursion depth

Note: To do this one, i needed to use Claude a lot.
"""

from functools import lru_cache


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """Recursion over indices with memoization (top-down DP)."""

        @lru_cache(maxsize=None)
        def _dp(i: int, j: int) -> bool:
            """Return True if s[i:] matches p[j:]."""

            # Base case: pattern exhausted -> match only if s is exhausted too.
            # (An exhausted s can still match a remaining pattern, e.g. "a*")
            if j == len(p):
                return i == len(s)

            # Does the current character of s match the current one of p?
            # Check i < len(s) first to avoid indexing past the end.
            first_match = i < len(s) and p[j] in (s[i], ".")

            # Is the current token of the form x*? Look at p[j + 1], not p[j].
            has_star = j + 1 < len(p) and p[j + 1] == "*"

            if has_star:
                # Option 1 (skip): jump over x* without consuming s.
                # Option 2 (consume one): consume s[i] and stay on the same token.
                return _dp(i, j + 2) or (first_match and _dp(i + 1, j))

            # Plain token: the character must match, then advance in both.
            return first_match and _dp(i + 1, j + 1)

        return _dp(0, 0)


if __name__ == "__main__":
    sol = Solution()
    # Examples from the problem statement
    assert not sol.isMatch("aa", "a")
    assert sol.isMatch("aa", "a*")
    assert sol.isMatch("ab", ".*")
    # Edge cases with empty strings
    assert sol.isMatch("", "")
    assert sol.isMatch("", "a*")
    assert not sol.isMatch("a", "")
    # A greedy approach fails here: a* must not consume every 'a'
    assert sol.isMatch("aaa", "a*a")
    # x* used zero times
    assert sol.isMatch("aab", "c*a*b")
    # Plain token that does not match
    assert not sol.isMatch("ba", "aa")
    assert sol.isMatch("aa", ".*")
    assert not sol.isMatch("mississippi", "mis*is*p*.")
    # Would be extremely slow without memoization
    assert not sol.isMatch("a" * 30, "a*" * 15 + "b")
    print("OK")
