"""
LeetCode 14 - Longest Common Prefix (Easy)

Problem: Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "".
Constraints: 1 <= len(strs) <= 200, 0 <= len(strs[i]) <= 200, lowercase English letters only.

Notation for the complexity analysis:
    k = number of words, m = length of the common prefix (m <= length of the shortest word).

Approach 1 - Vertical scanning, building the prefix (longestCommonPrefixFirstApproach):
    Key idea: take the first word as reference and, letter by letter, check that every other
    word has the same letter at that position. Stop as soon as a word is too short or has a
    different letter. Each letter that passes the check is added to the prefix.

    Complexity:
        Time:  O(m * k) -> for each of the (at most m + 1) positions, we compare against the
               other k - 1 words. With the constraints: at most 200 * 200 = 40 000 comparisons.
        Space: O(m) -> the prefix string being built.

    Note:
        - The length check must come BEFORE word[idx]: thanks to short-circuit evaluation of
          "or", word[idx] is never evaluated when the word is too short (no IndexError).
        - First draft bug: "while not IndexError" never runs, because IndexError is a class
          (truthy), so "not IndexError" is False. Loops do not catch exceptions; use an
          explicit check or try/except.
        - The return after the for loop is needed: it covers the case where the whole first
          word is the prefix (e.g. ["flow", "flower"]).

Approach 2 - Vertical scanning, slicing at the end (longestCommonPrefix):
    Key idea: same scan, but no prefix is built. When the check fails at position idx, the
    prefix is exactly first_word[:idx]; if it never fails, the prefix is the whole first word.

    Complexity:
        Time:  O(m * k) -> same scan as Approach 1.
        Space: O(1) extra -> only the index; the returned slice (O(m)) is the output itself.

    Note:
        - Avoids creating a new string on every "+=", since Python strings are immutable.
        - Same asymptotic time: the gain is less memory and simpler code.
"""


class Solution:
    def longestCommonPrefixFirstApproach(self, strs: list[str]) -> str:
        """Scan letter by letter, building the prefix as we go."""
        first_word = strs[0]
        other_words = strs[1:]
        prefix = ""

        for idx, letter in enumerate(first_word):
            for word in other_words:
                # Stop if the word is too short or the letter differs
                if idx >= len(word) or word[idx] != letter:
                    return prefix
            prefix += letter
        return prefix

    def longestCommonPrefix(self, strs: list[str]) -> str:
        """Scan letter by letter and slice the first word where the check fails."""
        first_word = strs[0]
        other_words = strs[1:]

        for idx, letter in enumerate(first_word):
            for word in other_words:
                # Stop if the word is too short or the letter differs
                if idx >= len(word) or word[idx] != letter:
                    return first_word[:idx]  # position idx not included
        return first_word  # the whole first word is the common prefix


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        (["flower", "flow", "flight"], "fl"),
        (["dog", "racecar", "car"], ""),  # no common prefix
        (["flower", "flow"], "flow"),  # another word is shorter than the first
        (["flow", "flower"], "flow"),  # the whole first word is the prefix
        (["a"], "a"),  # single word
        (["", "b"], ""),  # empty word
        (["ab", "a"], "a"),
        (["abc", "abc", "abc"], "abc"),  # identical words
    ]

    for method in (sol.longestCommonPrefixFirstApproach, sol.longestCommonPrefix):
        for strs, expected in test_cases:
            assert method(strs) == expected, (method.__name__, strs)
        print(f"{method.__name__}: OK")
