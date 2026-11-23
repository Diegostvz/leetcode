"""
LeetCode 35 - Search Insert Position (Easy)

Problem:
    Given a sorted array of distinct integers and a target value, return
    the index if the target is found. If not, return the index where it
    would be inserted to keep the array sorted. Must run in O(log n).

Approach 1 - Binary search returning lo

    Standard binary search: return mid if nums[mid] == target, otherwise
    discard the half where target cannot be. If the loop ends without a
    match, lo is the insertion position.

    Complexity (half of the search space is discarded each iteration):
        Time:  O(log n)
        Space: O(1)

    Note:
        - Invariant: everything left of lo is < target, everything right
          of hi is > target.
        - When the loop ends, hi = lo - 1, so lo is the first index with
          a value greater than target -> insertion position.
        - Returning hi is WRONG (e.g. [1, 3, 5, 6], target 0 -> hi = -1).
"""


class Solution:
    def searchInsert(self, nums: list[int], target: int) -> int:

        lo = 0
        hi = len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1

        return lo  # insertion position (hi = lo - 1 here)


if __name__ == "__main__":
    sol = Solution()

    assert sol.searchInsert([1, 3, 5, 6], 5) == 2  # found
    assert sol.searchInsert([1, 3, 5, 6], 2) == 1  # insert in the middle
    assert sol.searchInsert([1, 3, 5, 6], 7) == 4  # insert at the end
    assert sol.searchInsert([1, 3, 5, 6], 0) == 0  # insert at the start
    assert sol.searchInsert([1], 1) == 0
    assert sol.searchInsert([1], 2) == 1

    print("OK")
