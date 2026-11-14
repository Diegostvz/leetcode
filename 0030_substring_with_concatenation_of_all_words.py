"""
LeetCode 30 - Substring with Concatenation of All Words (Hard)

Problem: Given a string s and an array of strings words, all of the SAME length, return the
starting indices of all the substrings of s that are a concatenation of every word in words
exactly once, in any order (repeated words in words must appear the same number of times).
The answer can be returned in any order.
(1 <= len(s) <= 10^4, 1 <= len(words) <= 5000, 1 <= len(words[i]) <= 30, lowercase letters)

Approach 1 - Check every window with a Counter (findSubstringBruteForce):
    Key idea: generating permutations is hopeless (5000! orders), and the order does not
    matter anyway: a window is valid iff it contains the same words the same number of times.
    A valid window has length k * w, and since all words have length w, it can be split into
    k chunks without ambiguity. For every possible start, split the window and compare
    Counter(chunks) with Counter(words).

    Complexity (n = len(s), k = len(words), w = len(words[0])):
        Time:  O(n * k * w) -> about n starts; each one builds k slices of length w and hashes
               them into a Counter: O(k * w) per window.
        Space: O(k * w) -> the k chunks of the current window plus the target Counter.

    Note:
        - Counter(...) == Counter(...) checks the same keys AND the same counts at once,
          ignoring order: exactly the condition of the problem.
        - The last valid start is n - k * w, so the range is range(n - k * w + 1).

Approach 2 - Sliding window over words, one pass per offset (findSubstring):
    Key idea: two consecutive windows at distance w share k - 1 words, so recounting from
    scratch wastes work. Windows only share words if they are aligned, so split the starts
    into w groups by offset (0, 1, ..., w - 1). In each group, s is a sequence of words:

        offset 0: bar | foo | the | foo | bar | man
        offset 1:  arf | oot | hef | oob | arm
        offset 2:   rfo | oth | efo | oba | rma

    Walk each sequence with two pointers (left, right) and a Counter of the window:
        1. word not in target -> no window containing it can be valid: empty the window and
           move left right after it.
        2. word in target -> add it; while it appears MORE times than allowed, remove words
           from the left.
        3. window has exactly k words -> save left, then remove the leftmost word so the
           window can keep sliding.

    Complexity (n = len(s), k = len(words), w = len(words[0])):
        Time:  O(n * w) -> w offsets with about n / w words each; every word enters and leaves
               the window at most once: O(n) word operations, each O(w) (slice + hash).
               The factor k disappears.
        Space: O(k * w) -> the target Counter and the window Counter (at most k words).

    Note:
        - Same sliding-window pattern as LeetCode 3 (Longest Substring Without Repeating
          Characters), with words instead of characters.
        - A Counter returns 0 for missing keys, so window[word] needs no existence check.
"""

from collections import Counter


class Solution:
    def findSubstringBruteForce(self, s: str, words: list[str]) -> list[int]:
        """Split every possible window into k chunks and compare its Counter with words."""
        k = len(words)
        w = len(words[0])
        target = Counter(words)
        indices = []

        for start in range(len(s) - k * w + 1):
            chunks = []
            for i in range(k):
                chunks.append(s[start + i * w : start + (i + 1) * w])
            if Counter(chunks) == target:
                indices.append(start)
        return indices

    def findSubstring(self, s: str, words: list[str]) -> list[int]:
        """Slide a window of words over each of the w alignments of s."""
        k = len(words)
        w = len(words[0])
        target = Counter(words)
        indices = []

        for offset in range(w):  # one pass per alignment
            left = offset  # start of the current window
            window = Counter()  # words inside the current window
            count = 0  # number of words inside the current window

            for right in range(offset, len(s) - w + 1, w):  # one word at a time
                word = s[right : right + w]

                if word not in target:  # 1. invalid word: restart after it
                    window.clear()
                    count = 0
                    left = right + w
                    continue

                window[word] += 1  # 2. valid word: add it
                count += 1
                while (
                    window[word] > target[word]
                ):  # too many copies: shrink from the left
                    window[s[left : left + w]] -= 1
                    count -= 1
                    left += w

                if count == k:  # 3. full window: save it, then drop the leftmost word
                    indices.append(left)
                    window[s[left : left + w]] -= 1
                    count -= 1
                    left += w

        return indices


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("barfoothefoobarman", ["foo", "bar"], [0, 9]),
        ("wordgoodgoodgoodbestword", ["word", "good", "best", "word"], []),
        ("barfoofoobarthefoobarman", ["bar", "foo", "the"], [6, 9, 12]),
        (
            "wordgoodgoodgoodbestword",
            ["word", "good", "best", "good"],
            [8],
        ),  # repeated word
        ("aaaaaa", ["aa", "aa"], [0, 1, 2]),  # overlapping windows
        ("foo", ["foo", "bar"], []),  # s shorter than the window
        ("abababab", ["ab", "ba"], []),  # chunks must align to the window start
        ("a", ["a"], [0]),  # single character
        ("ababaab", ["ab", "ba", "ba"], [1]),  # shrinking from the left
    ]

    for method in (sol.findSubstringBruteForce, sol.findSubstring):
        for s, words, expected in test_cases:
            result = method(s, words)
            assert sorted(result) == sorted(expected), (
                method.__name__,
                s,
                words,
                result,
            )
        print(f"{method.__name__}: OK")

    # Cross-check both approaches on random inputs with a tiny alphabet (many matches)
    import random

    for _ in range(2000):
        w = random.randint(1, 3)
        words = [
            "".join(random.choices("ab", k=w)) for _ in range(random.randint(1, 4))
        ]
        s = "".join(random.choices("ab", k=random.randint(1, 20)))
        assert sorted(sol.findSubstring(s, words)) == sorted(
            sol.findSubstringBruteForce(s, words)
        ), (s, words)
    print("Both approaches agree on 2000 random cases")
