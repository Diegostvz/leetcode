"""
LeetCode 17 - Letter Combinations of a Phone Number (Medium)

Problem: Given a string digits containing digits from 2 to 9, return all possible letter
combinations that the number could represent, using the telephone keypad mapping
(2 -> abc, 3 -> def, 4 -> ghi, 5 -> jkl, 6 -> mno, 7 -> pqrs, 8 -> tuv, 9 -> wxyz).
The answer can be returned in any order. (0 <= len(digits) <= 4)

Approach 1 - Iterative cartesian product (letterCombinations):
    Key idea: the answer is the cartesian product of the letter groups of each digit.
    Start with [""] (one empty combination) and, for each digit, extend every combination
    built so far with every letter of that digit. The number of combinations is multiplied
    by the number of letters of each digit: 1 -> 3 -> 3*3 -> 3*3*4 -> ...
    If digits is empty, return [] (no combinations at all).

    Complexity (n = len(digits), worst case: every digit is 7 or 9, with 4 letters):
        Time:  O(n * 4^n) -> 4^n combinations in the output, each built by string
               concatenation of length up to n. The intermediate levels add
               4 + 16 + ... + 4^(n-1) < 4^n / 3 extra strings, so they do not change the order.
        Space: O(n * 4^n) -> the output itself (4^n strings of length n).
        With n <= 4: at most 4^4 = 256 strings, so it is constant in practice.

    Note:
        - This is optimal: the output alone has size n * 4^n, so no algorithm can do better.
        - The growth is EXPONENTIAL (4^n), not polynomial: O(n^5) would be a different and
          wrong order, even if the numbers look similar for small n.
        - Same result with the standard library: itertools.product(*groups), then "".join
          each tuple.
        - Recursive alternative: backtracking (depth-first over the same tree of choices),
          a pattern that appears in many combinatorial problems (subsets, permutations...).
        - str + str joins two strings; "".join(list) joins many. prefix.join(letter) is NOT
          concatenation: join uses the string before the dot as the separator.
"""


class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        """Build the cartesian product of the letter groups, one digit at a time."""
        if not digits:
            return []

        letters = (
            "abc",
            "def",
            "ghi",
            "jkl",
            "mno",
            "pqrs",
            "tuv",
            "wxyz",
        )  # digits 2..9
        result = [""]
        for digit in digits:
            new_result = []
            for prefix in result:
                for letter in letters[int(digit) - 2]:  # the letters of this digit
                    new_result.append(prefix + letter)  # extend the combination
            result = new_result  # the new level replaces the old one
        return result


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("23", ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]),
        ("", []),  # empty input
        ("2", ["a", "b", "c"]),  # single digit
        ("79", [p + w for p in "pqrs" for w in "wxyz"]),  # two 4-letter digits
        (
            "22",
            ["aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"],
        ),  # repeated digit
    ]

    for digits, expected in test_cases:
        assert sorted(sol.letterCombinations(digits)) == sorted(expected), digits

    # Size checks: product of the group sizes, all combinations distinct
    for digits, size in (("234", 27), ("9999", 256), ("2379", 3 * 3 * 4 * 4)):
        result = sol.letterCombinations(digits)
        assert len(result) == size and len(set(result)) == size, digits

    print("OK")
