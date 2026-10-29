"""
LeetCode 13 - Roman to Integer (Easy)

Problem: Seven symbols represent Roman numerals: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500,
M = 1000. Numerals are usually written from largest to smallest, except for six subtractive
pairs where a smaller symbol is placed before a larger one: IV = 4, IX = 9, XL = 40, XC = 90,
CD = 400, CM = 900. Given a valid Roman numeral s (1 <= len(s) <= 15, value in [1, 3999]),
convert it to an integer.

Approach 1 - Subtractive pairs in the table + skipping with the iterator (romanToIntFirstApproach):
    Key idea: store the 6 subtractive pairs in the table as if they were symbols. Look at s[i]
    and s[i + 1]: if s[i] < s[i + 1] they form a pair, so add the value of the pair and skip the
    next character by calling next() on the same iterator used by the for loop. Otherwise, add
    the value of s[i].

    Complexity:
        Time:  O(n), n = len(s) <= 15 -> constant in practice.
        Space: O(1) -> fixed-size table and a few variables.

    Note:
        - next() must be called on the iterator object itself (iter_enum_s), not on idx or char.
          Calling next(enumerate(s)) would create a NEW iterator and not affect the loop.
        - For the last character there is no s[i + 1]; using "I" as a sentinel works because
          nothing is smaller than I, so the last symbol is always simply added.
        - next() without a default is safe here: a pair is only detected when s[i + 1] exists.
        - Alternative without iterators: a while loop with a manual index (i += 2 on a pair).

Approach 2 - Sign of each symbol depends on the next one (romanToInt):
    Key idea: every symbol contributes on its own: it is SUBTRACTED if it is smaller than the
    symbol that follows it, and ADDED otherwise (the last symbol is always added).
    E.g. IV = -1 + 5, CM = -100 + 1000. Only the 7 basic symbols are needed: no pairs in the
    table, no skipping and no try/except.

    Complexity:
        Time:  O(n), n = len(s) <= 15 -> constant in practice.
        Space: O(1) -> fixed-size table and a few variables.

    Note:
        - Same asymptotic complexity as Approach 1: the gain is simplicity (smaller table, no
          special handling of pairs, no exceptions), not speed.
        - Equivalent right-to-left version: keep the previous value and subtract the current
          symbol if it is smaller than it. This avoids the "does a next element exist?" check.
"""


class Solution:
    def romanToIntFirstApproach(self, s: str) -> int:
        """Look up subtractive pairs in the table and skip their second character."""
        roman = {
            "M": 1000,
            "CM": 900,
            "D": 500,
            "CD": 400,
            "C": 100,
            "XC": 90,
            "L": 50,
            "XL": 40,
            "X": 10,
            "IX": 9,
            "V": 5,
            "IV": 4,
            "I": 1,
        }
        result = 0
        iter_enum_s = enumerate(s)  # named so we can call next() on it inside the loop
        for idx, char in iter_enum_s:
            try:
                next_char = s[idx + 1]
            except IndexError:
                next_char = "I"  # sentinel: the last symbol is always added
            if roman[char] < roman[next_char]:
                result += roman[char + next_char]
                next(iter_enum_s)  # skip the second character of the pair
            else:
                result += roman[char]
        return result

    def romanToInt(self, s: str) -> int:
        """Add or subtract each symbol depending on the symbol that follows it."""
        roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        length = len(s)
        result = 0

        for idx, char in enumerate(s):
            # Subtract only if a next symbol exists and it is larger than the current one
            if idx + 1 < length and roman[char] < roman[s[idx + 1]]:
                result -= roman[char]
            else:
                result += roman[char]
        return result


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("III", 3),
        ("LVIII", 58),
        ("MCMXCIV", 1994),  # three subtractive pairs
        ("I", 1),  # single symbol
        ("IV", 4),  # pair at the end
        ("IX", 9),
        ("XL", 40),
        ("XC", 90),
        ("CD", 400),
        ("CM", 900),
        ("MMMCMXCIX", 3999),  # upper bound
        ("MMMDCCCLXXXVIII", 3888),  # longest input (15 symbols)
    ]

    for method in (sol.romanToIntFirstApproach, sol.romanToInt):
        for roman_numeral, expected in test_cases:
            assert method(roman_numeral) == expected, (method.__name__, roman_numeral)
        print(f"{method.__name__}: OK")
