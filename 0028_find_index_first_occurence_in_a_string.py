"""
LeetCode 28 - Find the Index of the First Occurrence in a String (Easy)

Problem: Given two strings needle and haystack, return the index of the first occurrence of
needle in haystack, or -1 if needle is not part of haystack.
(1 <= len(haystack), len(needle) <= 10^4, lowercase English letters only)

Approach 1 - Sliding window, character by character (strStr):
    Key idea: try every possible start of needle inside haystack, from 0 to
    len(haystack) - len(needle) (both included). For each start, compare needle with the
    window of haystack character by character and stop at the first mismatch. If the whole
    window matches, that start is the answer.

    Complexity (h = len(haystack), n = len(needle)):
        Time:  O(h * n) -> (h - n + 1) starts, up to n comparisons each:
               (h - n + 1) * n <= h * n.
               Worst case: almost-matches everywhere, e.g. "aaaaab" with "aab".
               If n = 1 it is just O(h): keep both sizes, do not simplify to O(h^2).
        Space: O(1) -> two indices.

    Note:
        - for ... else: the else runs only if the loop finished WITHOUT break, i.e. every
          character matched. A return placed right after the inner loop would run even after
          a break.
        - break only exits the INNER loop; the outer loop continues with the next start.
        - The last valid start is h - n, so the range is range(h - n + 1). If n > h the range
          is empty and -1 is returned with no special case.
        - Same complexity, faster in practice: compare slices, haystack[start:start + n] ==
          needle (the comparison runs in C). The built-in is haystack.find(needle).
        - Optimal: KMP (Knuth-Morris-Pratt) runs in O(h + n) by never re-reading haystack
          characters after a partial match.
"""


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        """Try every start and compare the window with needle until the first mismatch."""
        for start in range(len(haystack) - len(needle) + 1):  # every possible start
            for offset in range(len(needle)):  # position inside needle
                if needle[offset] != haystack[start + offset]:
                    break  # mismatch: try the next start
            else:
                return start  # no break: the whole window matches
        return -1


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("sadbutsad", "sad", 0),  # first of two occurrences
        ("leetcode", "leeto", -1),
        ("pepito", "pepe", -1),
        ("hello", "ll", 2),
        ("abc", "c", 2),  # match at the very end
        ("abc", "abc", 0),  # needle == haystack
        ("a", "ab", -1),  # needle longer than haystack
        ("a", "a", 0),  # single character
        ("mississippi", "issip", 4),  # partial matches before the real one
        ("aaaaab", "aab", 3),  # worst case for the window check
        ("a" * 9999 + "b", "a" * 5000 + "b", 4999),  # max size, worst case
    ]

    for haystack, needle, expected in test_cases:
        result = sol.strStr(haystack, needle)
        assert result == expected, (haystack[:20], needle[:20], result)
        assert result == haystack.find(needle)  # same as the built-in
    print("OK")
