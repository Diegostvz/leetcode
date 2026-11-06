"""
LeetCode 22 - Generate Parentheses (Medium)

Problem:

Approach 1 - Iterative process for producing the combinations(from i = 1 to i = n), begin with i = 1 -- {"()"}, IMPORTANT TO PRODUCE SETS
TO AVOID REPETITIONS, then for every new i, join each element from the previuos set a new pair in three possible ways:

1 - Join opener by left side, and closer by right side --- Sandwich
2 - Join opener + closer by left side --- LeftSided-Append
3 - Join opener + closer by right side --- RightSided-Append

When finished transform the set into a list to match the desired type of output.

    Complexity:
        Time:  O()
        Space: O(3^(n-1)) worst case

    Note:

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
        """"""
        n_active_openers = 0
        for _ in range(2 * n):
            new = set()
            for combination in current:
                for pos in range(len(combination) + 1):
                    new.add(combination[:pos] + "()" + combination[pos:])
            current = new
        return list(current)


if __name__ == "__main__":
    sol = Solution()
    assert sorted(sol.generateParenthesis(n=1)) == sorted(["()"])
    assert sorted(sol.generateParenthesis(n=2)) == sorted(["(())", "()()"])
    assert sorted(sol.generateParenthesis(3)) == sorted(
        ["((()))", "(()())", "(())()", "()(())", "()()()"]
    )
    assert "(())(())" in sol.generateParenthesis(4)
    for n, catalan in ((1, 1), (2, 2), (3, 5), (4, 14), (5, 42), (8, 1430)):
        result = sol.generateParenthesis(n)
        assert len(result) == catalan and len(set(result)) == catalan, n
    print("OK")
