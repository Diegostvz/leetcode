"""
LeetCode 22 - Generate Parentheses (Medium)

Problem: Given n pairs of parentheses, write a function to generate all combinations of
well-formed parentheses. (1 <= n <= 8)
The number of combinations is the n-th Catalan number: C_n = (2n choose n) / (n + 1)
-> 1, 2, 5, 14, 42, 132, 429, 1430, ...  Asymptotically, C_n ~ 4^n / (n^(3/2) * sqrt(pi)).

Approach 1 - Insert "()" at every position, level by level (generateParenthesisInsertion):
    Key idea: every valid string with n pairs contains an adjacent "()" somewhere; removing it
    leaves a valid string with n - 1 pairs. Conversely, inserting "()" at EVERY position of
    EVERY valid string with n - 1 pairs produces all valid strings with n pairs.
    Start with {"()"} and repeat n - 1 times. A set removes the many duplicates.

    Complexity:
        Time:  O(sqrt(n) * 4^n) -> the last level dominates: C_(n-1) strings, 2n - 1
               insertion positions each, and every insertion builds a new string of length 2n:
               C_(n-1) * 2n * 2n ~ (4^n / n^(3/2)) * n^2 = sqrt(n) * 4^n.
        Space: O(n * C_n) = O(4^n / sqrt(n)) -> the set of C_n strings of length 2n.

    Note:
        - First idea (sandwich + append "()" on the left + on the right) is INCOMPLETE: from
          n = 4 it misses concatenations of blocks, e.g. "(())(())". Those three rules are just
          special cases of inserting "()" at some position.
        - Each string is generated many times (once per "()" it contains): the set discards the
          duplicates AFTER doing the work.

Approach 2 - Backtracking with pruning (generateParenthesis):
    Key idea: build the string one character at a time. At each step there are only two
    options, and each one is only allowed if it can still lead to a valid string:
        - add "(" if open_count < n           (there are openers left)
        - add ")" if close_count < open_count (there is something open to close)
    When the string has 2n characters it is valid by construction: save it and go back.
    Invalid prefixes are never built, so there are no duplicates and no set is needed.

    Complexity:
        Time:  O(4^n / sqrt(n)) -> the recursion tree has C_n leaves (one per answer), and
               building/saving each answer costs O(n): C_n * n ~ 4^n / sqrt(n).
               The internal nodes are valid prefixes shared by many answers, so they do not
               change the order.
        Space: O(n) auxiliary -> recursion depth is 2n (one level per character).
               The output itself is O(n * C_n).

    Note:
        - Both if's are independent (not if/elif): when both options are allowed, BOTH
          branches must be explored.
        - Counters are passed as new values (open_count + 1) instead of being modified, so
          sibling branches always start from the same state and nothing has to be undone.
        - Better than Approach 1 by a factor of n in time, and O(n) vs exponential extra space.
        - Backtracking template: if complete -> save and return; for each option, if allowed
          (pruning) -> recurse with the updated state.
"""


class Solution:
    def generateParenthesisInsertion(self, n: int) -> list[str]:
        """Build level i from level i - 1 by inserting "()" at every position."""
        current = {"()"}
        for _ in range(n - 1):
            new = set()
            for combination in current:
                for pos in range(len(combination) + 1):
                    new.add(combination[:pos] + "()" + combination[pos:])
            current = new
        return list(current)

    def generateParenthesis(self, n: int) -> list[str]:
        """Add one bracket at a time, only if the prefix can still become valid."""
        combinations = []

        def _backtrack(current: str, open_count: int, close_count: int) -> None:
            if len(current) == 2 * n:  # complete: valid by construction
                combinations.append(current)
                return

            if open_count < n:  # openers left
                _backtrack(current + "(", open_count + 1, close_count)
            if close_count < open_count:  # something open to close
                _backtrack(current + ")", open_count, close_count + 1)

        _backtrack("", 0, 0)
        return combinations


if __name__ == "__main__":
    sol = Solution()

    for method in (sol.generateParenthesisInsertion, sol.generateParenthesis):
        assert sorted(method(1)) == ["()"]
        assert sorted(method(2)) == sorted(["(())", "()()"])
        assert sorted(method(3)) == sorted(
            ["((()))", "(()())", "(())()", "()(())", "()()()"]
        )
        assert "(())(())" in method(4)  # the case the first idea missed

        # Count must be the Catalan number, with no duplicates
        for n, catalan in ((1, 1), (2, 2), (3, 5), (4, 14), (5, 42), (8, 1430)):
            result = method(n)
            assert len(result) == catalan and len(set(result)) == catalan, (
                method.__name__,
                n,
            )
        print(f"{method.__name__}: OK")

    # Both approaches must produce exactly the same set
    for n in range(1, 9):
        assert set(sol.generateParenthesisInsertion(n)) == set(
            sol.generateParenthesis(n)
        ), n
    print("Both approaches agree for n = 1..8")
