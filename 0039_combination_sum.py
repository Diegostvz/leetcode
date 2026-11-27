"""
LeetCode 39 - Combination Sum (Medium)

Problem:
    Given an array of distinct integers candidates and a target integer,
    return a list of all unique combinations of candidates where the
    chosen numbers sum to target. The same number may be chosen an
    unlimited number of times. Two combinations are unique if the
    frequency of at least one chosen number differs. Order of the output
    does not matter.

Approach 1 - Backtracking with start index + pruning

    Sort candidates, then backtrack(start, remaining):
    1. remaining == 0 -> save a COPY of the current combination.
    2. For i from start: if candidates[i] > remaining, break (sorted, so
       every later candidate is bigger too -> pruning).
    3. Choose candidates[i], explore with backtrack(i, remaining - c),
       then undo (pop).
    Passing i (not i + 1) allows reusing the same number; never going
    back below start keeps every combination in non-decreasing order, so
    [2, 2, 3] is generated once and [2, 3, 2] / [3, 2, 2] never appear.

    Complexity (n = len(candidates), T = target, m = min(candidates)):
        Time:  O(n^(T/m + 1)) -> the tree has depth at most T/m and up to
               n branches per node (loose upper bound; pruning helps a lot).
        Space: O(T/m) recursion depth and current combination
               (output list not counted).

    Note:
        - Template for backtracking: choose -> explore -> undo.
        - Save combination.copy(): saving the list itself stores a
          reference that later pops will empty.
        - Pass remaining - elem to the call; doing remaining -= elem
          corrupts the value for the next iterations of the loop.
        - start index removes duplicate permutations of the same
          combination; i vs i + 1 decides if reuse is allowed
          (LeetCode 40 uses i + 1).
"""


class Solution:
    def combinationSum(self, candidates: list[int], target: int) -> list[list[int]]:

        candidates = sorted(candidates)

        combinations = []
        combination = []

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                combinations.append(combination.copy())
                return

            for i in range(start, len(candidates)):
                elem = candidates[i]
                if elem > remaining:
                    break  # sorted -> every later candidate overshoots too
                combination.append(elem)  # choose
                backtrack(i, remaining - elem)  # explore (same i: reuse allowed)
                combination.pop()  # undo

        backtrack(0, target)
        return combinations


if __name__ == "__main__":
    sol = Solution()

    cases = (
        ([2, 3, 6, 7], 7, [[2, 2, 3], [7]]),
        ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]]),
        ([2], 1, []),
        ([1], 2, [[1, 1]]),
        ([7, 3, 2, 6], 7, [[2, 2, 3], [7]]),  # unsorted input
    )

    for candidates, target, expected in cases:
        result = sol.combinationSum(candidates, target)
        assert sorted(result) == sorted(expected), f"{candidates}, {target}"
        assert len(result) == len({tuple(c) for c in result}), "duplicates"

    print("OK")
