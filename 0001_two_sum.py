"""
LeetCode 1 - Two Sum (Easy)

Problem: Given an array of integers nums and an integer target, return the indices of the two
numbers such that they add up to target. Each input has exactly one solution, and the same
element may not be used twice. The answer can be returned in any order.
(2 <= len(nums) <= 10^4, -10^9 <= nums[i], target <= 10^9)

Approach 1 - Sort + two pointers (twoSumTwoPointers):
    Key idea: in a sorted array, if nums[l] + nums[r] is too small, only moving l to the right
    can increase the sum; if it is too large, only moving r to the left can decrease it. So
    every step discards one element, and the pair is found in a single sweep.
    Since the problem asks for ORIGINAL indices, we sort the indices by their value instead of
    sorting nums itself.

    Complexity:
        Time:  O(n log n) -> dominated by the sort; the two-pointer sweep is O(n).
        Space: O(n) -> the sorted list of indices.

    Note:
        - Sorting nums directly (nums = sorted(nums)) loses the original positions, so the
          returned indices point to the sorted array, not to the input.
          E.g. nums = [3, 2, 4], target = 6 -> sorted [2, 3, 4] -> returns [0, 2] (wrong, the
          answer is [1, 2]).
        - This approach is optimal for LeetCode 167 (Two Sum II), where the input is ALREADY
          sorted: no sort is needed and it runs in O(n) time and O(1) space.

Approach 2 - One-pass hash map / complement lookup (twoSum):
    Key idea: store each number already seen in a dict {value: index}. For each x, check whether
    its complement (target - x) has already been seen; if so, the pair is found.

    Complexity:
        Time:  O(n) -> one pass, O(1) average dict lookup and insert.
        Space: O(n) -> the dict may store up to n - 1 numbers.

    Note:
        - Checking the complement BEFORE inserting the current number prevents using the same
          element twice (e.g. nums = [3, 5], target = 6 must not return [0, 0]).
        - Duplicates work: in nums = [3, 3], the first 3 is stored, and the second finds it.
        - Baseline for comparison: brute force over every pair is O(n^2) time, O(1) space.
"""


class Solution:
    def twoSumTwoPointers(self, nums: list[int], target: int) -> list[int]:
        """Sort the indices by value and close in with two pointers."""
        order = sorted(
            range(len(nums)), key=lambda i: nums[i]
        )  # original indices, by value
        l, r = 0, len(nums) - 1
        while l < r:
            current = nums[order[l]] + nums[order[r]]
            if current == target:
                return sorted([order[l], order[r]])
            elif current < target:
                l += 1  # need a larger sum
            else:
                r -= 1  # need a smaller sum
        return []  # unreachable: the problem guarantees exactly one solution

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        """Look up each number's complement among the numbers already seen."""
        seen = {}  # value -> index
        for i, x in enumerate(nums):
            complement = target - x
            if complement in seen:
                return [seen[complement], i]
            seen[x] = i
        return []  # unreachable: the problem guarantees exactly one solution


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),  # sorting changes the order: catches the lost-index bug
        ([3, 3], 6, [0, 1]),  # duplicates
        ([3, 5], 8, [0, 1]),  # minimum length
        ([1, 5, 3], 6, [0, 1]),  # 3 + 3 = 6 must NOT use the same element twice
        ([-1, -2, -3, -4, -5], -8, [2, 4]),  # negatives
        ([0, 4, 3, 0], 0, [0, 3]),  # zeros
        ([5, 1, 9, 2, 8], 13, [0, 4]),  # pair at both ends of the input
        ([10**9, -(10**9), 7], 0, [0, 1]),  # value bounds
    ]

    for method in (sol.twoSumTwoPointers, sol.twoSum):
        for nums, target, expected in test_cases:
            result = sorted(method(nums, target))  # any order is accepted
            assert result == expected, (method.__name__, nums, target, result)
        print(f"{method.__name__}: OK")
