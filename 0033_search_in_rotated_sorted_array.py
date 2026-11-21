"""
LeetCode 33 - Search In Rotated Sorted Array (Medium)

Problem:
    Given an integer array nums sorted in ascending order (with distinct
    values) and possibly rotated at an unknown pivot, return the index of
    target in nums, or -1 if it is not present. Must run in O(log n).

Approach 1 - Modified binary search

    At every step, at least one of the two halves [lo..mid] or [mid..hi]
    is sorted (the rotation can only break one of them).
    1. Check if nums[mid] is the target.
    2. Find the sorted half: if nums[lo] <= nums[mid], the left half is
       sorted; otherwise the right half is.
    3. If target lies within the range of the sorted half, search there;
       otherwise discard it and search the other half.

    Complexity (half of the search space is discarded each iteration):
        Time:  O(log n)
        Space: O(1)

    Note:
        - Use <= in nums[lo] <= nums[mid]: when lo == mid the left half has
          a single element and counts as sorted (fails on [3, 1] with <).
        - Checking if target is in a sorted half always needs TWO bounds:
          nums[lo] <= target < nums[mid] or nums[mid] < target <= nums[hi].
        - Only the sorted half gives reliable information; the unsorted
          half is chosen by elimination.
"""


class Solution:
    def search(self, nums: list[int], target: int) -> int:

        lo = 0
        hi = len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid

            if nums[lo] <= nums[mid]:  # left half sorted
                if nums[lo] <= target < nums[mid]:  # target in [nums[lo], nums[mid])
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:  # right half sorted
                if nums[mid] < target <= nums[hi]:  # target in (nums[mid], nums[hi]]
                    lo = mid + 1
                else:
                    hi = mid - 1

        return -1


if __name__ == "__main__":
    sol = Solution()

    assert sol.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert sol.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert sol.search([6, 7, 0, 1, 2, 4, 5], 7) == 1  # right half sorted
    assert sol.search([3, 1], 1) == 1  # lo == mid edge case
    assert sol.search([1], 0) == -1
    assert sol.search([1], 1) == 0
    assert sol.search([1, 2, 3, 4, 5], 4) == 3  # no rotation

    print("OK")
