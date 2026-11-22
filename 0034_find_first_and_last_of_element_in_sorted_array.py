"""
LeetCode 34 - Find First And Last Position Of Element In Sorted Array (Medium)

Problem:
    Given an array of integers nums sorted in non-decreasing order, find the
    starting and ending position of a given target value. If target is not
    found, return [-1, -1]. Must run in O(log n).

Approach 1 - Two binary searches (lower and upper bound)

    Run binary search twice with a helper find_bound:
    - When nums[mid] == target, save mid as candidate and keep searching:
      to the left (hi = mid - 1) for the first occurrence, or to the
      right (lo = mid + 1) for the last occurrence.
    - Otherwise, standard binary search.
    The last saved candidate is the answer (-1 if target never found).

    Complexity (two independent binary searches):
        Time:  O(log n)
        Space: O(1)

    Note:
        - Finding target and expanding one by one from mid is O(n) in the
          worst case (e.g. [8, 8, 8, 8], target 8).
        - Never slice the list in binary search: it breaks the original
          indices and costs O(n). Move lo / hi only.
        - Discarding mid after a match is safe because it is stored
          in candidate.
"""


class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:

        def find_bound(first: bool) -> int:
            lo, hi = 0, len(nums) - 1
            candidate = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if nums[mid] == target:
                    candidate = mid
                    if first:
                        hi = mid - 1  # look for an earlier occurrence
                    else:
                        lo = mid + 1  # look for a later occurrence
                elif nums[mid] < target:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return candidate

        left = find_bound(first=True)
        if left == -1:
            return [-1, -1]  # target not in nums, skip second search
        return [left, find_bound(first=False)]


if __name__ == "__main__":
    sol = Solution()

    assert sol.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert sol.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert sol.searchRange([], 0) == [-1, -1]
    assert sol.searchRange([8, 8, 8, 8], 8) == [0, 3]  # worst case for expansion
    assert sol.searchRange([1], 1) == [0, 0]

    print("OK")
