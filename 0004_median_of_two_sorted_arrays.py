"""
0004. Median of Two Sorted Arrays — Hard
https://leetcode.com/problems/median-of-two-sorted-arrays/
Pattern: binary search on partition
Complexity: O(log(min(m, n))) time, O(1) space
Notes:
- First approach: merge and sort, then take the middle element(s).
  O((m + n) log(m + n)) time, O(m + n) space. Accepted, but the problem
  explicitly asks for O(log(m + n)).
- Final approach: split both arrays into a left half and a right half so that
  the left half has (m + n + 1) // 2 elements and every left element <= every
  right element. Binary search only over how many elements i come from nums1;
  the rest j = half - i come from nums2.
- Valid partition: left1 <= right2 and left2 <= right1.
  If left1 > right2, take fewer from nums1 (hi = i - 1); otherwise take more.
- Search over the shorter array so that j never goes out of range.
- -inf / inf sentinels handle partitions at the edges (i = 0, i = m, ...).
"""

from math import inf


class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        half = (m + n + 1) // 2
        lo, hi = 0, m

        while lo <= hi:
            i = (lo + hi) // 2  # elements taken from nums1
            j = half - i  # elements taken from nums2

            left1 = nums1[i - 1] if i > 0 else -inf
            right1 = nums1[i] if i < m else inf
            left2 = nums2[j - 1] if j > 0 else -inf
            right2 = nums2[j] if j < n else inf

            if left1 <= right2 and left2 <= right1:
                if (m + n) % 2 == 1:
                    return float(max(left1, left2))
                return (max(left1, left2) + min(right1, right2)) / 2
            elif left1 > right2:
                hi = i - 1
            else:
                lo = i + 1

        raise ValueError("Input arrays are not sorted")


if __name__ == "__main__":
    sol = Solution()
    assert sol.findMedianSortedArrays([1, 3], [2]) == 2.0
    assert sol.findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    assert sol.findMedianSortedArrays([], [1]) == 1.0
    assert sol.findMedianSortedArrays([2], []) == 2.0
    assert sol.findMedianSortedArrays([1, 2, 3, 4, 5], [6, 7]) == 4.0
    print("OK")
