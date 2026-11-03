"""
LeetCode 18 - 4Sum (Medium)

Problem: Given an array nums of n integers and an integer target, return all the unique
quadruplets [nums[a], nums[b], nums[c], nums[d]] such that a, b, c, d are distinct indices
and their sum equals target. The answer can be returned in any order.
(1 <= len(nums) <= 200, -10^9 <= nums[i], target <= 10^9)

Approach 1 - Sort + two fixed indices + two pointers (fourSum):
    Key idea: sort nums. Fix the first two numbers with two nested loops (i < j), so the
    problem reduces to Two Sum II on the sorted suffix nums[j + 1:] with
    newtarget = target - nums[i] - nums[j], solved with two pointers l and r.
    After a match, move both pointers and skip the values just used, so the same pair of
    values is not counted again. A set of tuples removes any remaining duplicates.

    Complexity:
        Time:  O(n^3) -> two nested loops over (i, j), O(n^2) pairs, and an O(n) two-pointer
               sweep for each pair. The O(n log n) sort does not change the order.
        Space: O(n) -> the sorted copy of nums (output not counted).

    Note:
        - j must start at i + 1: starting at i (or lower) reuses the same element,
          e.g. [1, 2, 3, 4] with target 7 would return [1, 1, 2, 3].
        - When skipping duplicates, compare with the value JUST USED (nums[l - 1],
          nums[r + 1]), not with the next one: skipping ahead can jump over a valid pair,
          e.g. [-4, -3, 0, 2, 2, 4] with target -3 loses [-4, -3, 2, 2].
        - If target < 0 and nums[0] >= 0, no quadruplet can reach target: early exit.
        - Generalizes kSum: fix k - 2 numbers with loops, then two pointers -> O(n^(k-1)).
"""


class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        n = len(nums)
        soluciones = set()
        nums = sorted(nums)

        for i in range(n - 2):
            if target < 0 and 0 <= nums[0]:
                return [list(tupla) for tupla in soluciones]
            else:
                for j in range(i + 1, n - 1):
                    newtarget = target - (nums[i] + nums[j])

                    l = j + 1
                    r = n - 1

                    while l < r:
                        if nums[l] + nums[r] == newtarget:
                            soluciones.add((nums[i], nums[j], nums[l], nums[r]))
                            l += 1
                            r -= 1
                            # skip values equal to the ones just used
                            while l < r and nums[l] == nums[l - 1]:
                                l += 1
                            while l < r and nums[r] == nums[r + 1]:
                                r -= 1
                        elif nums[l] + nums[r] < newtarget:
                            l += 1
                        else:
                            r -= 1
        return [list(tupla) for tupla in soluciones]


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 0, -1, 0, -2, 2], 0, [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
        ([2, 2, 2, 2, 2], 8, [[2, 2, 2, 2]]),  # all duplicates
        (
            [-4, -3, 0, 2, 2, 4],
            -3,
            [[-4, -3, 0, 4], [-4, -3, 2, 2]],
        ),  # duplicate-skip bug
        ([1, 2, 3, 4], 7, []),  # must not reuse the same element
        ([1, 2, 3, 4], 10, [[1, 2, 3, 4]]),  # exactly four elements
        ([1, 2, 3], 6, []),  # fewer than four elements
        ([0, 0, 0, 0], 0, [[0, 0, 0, 0]]),
        ([-2, -1, -1, 1, 1, 2, 2], 0, [[-2, -1, 1, 2], [-1, -1, 1, 1]]),
        ([-5, -4, -3, -2], -14, [[-5, -4, -3, -2]]),  # negative target
        ([10**9] * 4, 4 * 10**9, [[10**9] * 4]),  # value bounds
    ]

    for nums, target, expected in test_cases:
        result = sorted(sol.fourSum(nums, target))  # any order is accepted
        assert result == sorted(expected), (nums, target, result)
    print("OK")
