"""
LeetCode 12 - Integer to Roman (Medium)

Problem: Seven symbols represent Roman numerals: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500,
M = 1000. Numerals are formed by writing symbols from largest to smallest. When a decimal place
starts with 4 or 9, the subtractive form is used: a smaller symbol placed before a larger one
(IV = 4, IX = 9, XL = 40, XC = 90, CD = 400, CM = 900). Only powers of 10 (I, X, C, M) can be
repeated, at most 3 times. Given an integer 1 <= num <= 3999, convert it to a Roman numeral.

Approach 1 - Digit-by-digit with the subtractive rule (intToRomanFirstApproach):
    Key idea: look at the leading digit of the remaining number.
        - If it is not 4 or 9: append the largest symbol whose value is <= the remaining number
          and subtract its value.
        - If it is 4 or 9: apply the subtractive rule. The symbol in front is always the power
          of 10 of the same order as the number (10^(order - 1)), and the symbol behind is the
          first one whose value is greater than the "round" number (e.g. 40 -> L, 9 -> X).
          Append both and subtract (larger - smaller).
    Repeat until the remaining number is 0.

    Complexity:
        Time:  O(1) -> num <= 3999, so the output has at most 15 symbols (MMMDCCCLXXXVIII) and
               each iteration loops over a 7-entry dict. Without the upper bound, the loop would
               run O(num / 1000) times because of the repeated M's.
        Space: O(1) -> fixed-size dict and a few variables (the output is at most 15 chars).

    Note: bugs found while debugging:
        - str.join() is NOT concatenation: "MM".join("C") == "C". Use + / += instead.
        - "Largest symbol <= remaining", not "<": with "<", 10 became VIIIII.
        - In the subtractive case the front symbol is the power of 10 (9 -> IX, not VX).

Approach 2 - Greedy over a table that includes the subtractive pairs (intToRoman):
    Key idea: add the six subtractive pairs (CM, CD, XC, XL, IX, IV) to the table as if they were
    regular symbols, so 4 and 9 are no longer special cases. With the 13 entries sorted from
    largest to smallest, go through them once: for each symbol, append it as many times as it
    fits in the remaining number and subtract. No digits, str() or orders of magnitude needed.

    Complexity:
        Time:  O(1) -> one pass over a fixed 13-entry table, and the output has at most 15 symbols.
        Space: O(1) -> fixed-size table and a few variables.

    Note:
        - divmod(remaining, value) returns (how many times the symbol fits, what is left) in one
          step. Equivalent to: while value <= remaining: result += symbol; remaining -= value
        - Recurring bug: "fits" means <=, not <. With "<", num = 1 never matched and the outer
          while loop of a first draft ran forever.
        - Relies on dicts keeping insertion order (guaranteed since Python 3.7). A list of
          (value, symbol) tuples would make the ordering explicit.
"""


class Solution:
    def intToRomanFirstApproach(self, num: int) -> str:
        """Digit-by-digit conversion, handling 4 and 9 with the subtractive rule."""
        roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

        result = ""
        next_symbol = ""
        remaining = num

        while remaining > 0:
            remaining_str = str(remaining)

            if remaining_str[0] not in ("4", "9"):
                # Find the largest symbol whose value is <= remaining
                for symbol, value in roman.items():
                    if value <= remaining:
                        next_symbol = symbol
                    else:
                        break
                result += next_symbol
                remaining -= roman[next_symbol]

            else:  # Leading digit is 4 or 9 -> subtractive rule
                order = len(remaining_str)
                round_number = int(remaining_str[0] + "0" * (order - 1))
                for symbol, value in roman.items():
                    if value <= round_number:
                        # Front symbol: the power of 10 of the same order
                        if value == 10 ** (order - 1):
                            prev_symbol = symbol
                    else:
                        # Back symbol: first one greater than the round number
                        next_symbol = symbol
                        break
                result += prev_symbol + next_symbol
                remaining -= roman[next_symbol] - roman[prev_symbol]

        return result

    def intToRoman(self, num: int) -> str:
        """Greedy conversion over a descending table of values."""
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
        result = ""
        remaining = num
        for symbol, value in roman.items():
            # How many times the symbol fits, and what is left after using it
            count, remaining = divmod(remaining, value)
            result += symbol * count
        return result


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        (3749, "MMMDCCXLIX"),
        (58, "LVIII"),
        (1994, "MCMXCIV"),
        (1, "I"),
        (10, "X"),  # exact symbol value (<= vs <)
        (9, "IX"),  # subtractive: front symbol is a power of 10
        (90, "XC"),
        (4, "IV"),
        (400, "CD"),
        (900, "CM"),
        (3999, "MMMCMXCIX"),  # upper bound
        (3888, "MMMDCCCLXXXVIII"),  # longest output (15 symbols)
    ]

    for method in (sol.intToRomanFirstApproach, sol.intToRoman):
        for num, expected in test_cases:
            assert method(num) == expected, (method.__name__, num, method(num))
        print(f"{method.__name__}: OK")
