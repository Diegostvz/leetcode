"""
LeetCode 11 - Container With Most Water (Medium)

Problem: You are given an integer array height of length n. There are n vertical lines drawn such that
the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the
x-axis form a container, such that the container contains the most water. Return the maximum amount of
water a container can store. Notice that you may not slant the container.

Approach 1 - Brute force (maxAreaBruteForce):
    Key idea: the area of a pair (i, j) is the same as the area of (j, i), so we only need to check
    each pair once. For every line i we compute the area with every line j = i + 1, ..., n - 1 and
    keep the maximum.
    Area of a pair = width * height = (j - i) * min(height[i], height[j]).

    Complexity:
        Time:  O(n^2) -> the outer loop runs n - 1 times and the inner one n - i - 1 times,
               so the total is (n - 1) + (n - 2) + ... + 1 = n(n - 1) / 2 pairs.
        Space: O(n) -> height[i + 1:] creates a copy of the array on each outer iteration
               (only one copy is alive at a time). Without the slice it would be O(1).

    Note: correct, but too slow for n = 10^5 (~5 * 10^9 pairs) -> Time Limit Exceeded.
          A first version that stored every area in a list gave Memory Limit Exceeded.

Approach 2 - Two pointers (maxArea):
    Key idea: start with l and r at both ends (maximum possible width) and, after computing the
    area, move inwards the pointer with the SMALLER height.
    Why moving the taller one is useless: the water level is bounded above by the shorter line
    (min(height[l], height[r])) and the width decreases, so every new area would be smaller.
    Why discarding the shorter one is safe: any container using the shorter line with an inner
    line has a height <= the shorter line and a smaller width, so none of them can beat the area
    we just computed. We have already seen its best container, so we lose nothing.
    If both heights are equal, moving either pointer is fine.

    Complexity:
        Time:  O(n) -> each iteration moves exactly one pointer one step inwards, so the loop
               always runs n - 1 times (not only in the worst case).
        Space: O(1) -> only a few integer variables.

    Note: classic two-pointer pattern on a sorted-by-position range: start at both ends and
          discard, at each step, the element that can no longer be part of a better answer.
"""


class Solution:
    def maxAreaBruteForce(self, height: list[int]) -> int:
        """Check every pair of lines once and keep the largest area."""
        max_area = 0
        for i, left_height in enumerate(height[:-1]):
            # j is an offset from i: the second line is at position i + j + 1
            for j, right_height in enumerate(height[i + 1 :]):
                width = j + 1
                water_level = min(left_height, right_height)
                max_area = max(max_area, width * water_level)
        return max_area

    def maxArea(self, height: list[int]) -> int:
        """Two pointers moving inwards from both ends."""
        max_area = 0
        l, r = 0, len(height) - 1
        while l < r:
            width = r - l
            water_level = min(height[l], height[r])
            max_area = max(max_area, width * water_level)
            # Discard the shorter line: it cannot form a better container
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return max_area


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 1], 1),
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([4, 3, 2, 1, 4], 16),  # best pair is at both ends
        ([1, 2, 1], 2),
        ([2, 3, 4, 5, 18, 17, 6], 17),  # best pair is two tall adjacent lines
    ]

    for method in (sol.maxAreaBruteForce, sol.maxArea):
        for height, expected in test_cases:
            assert method(height) == expected, (method.__name__, height)
        print(f"{method.__name__}: OK")
