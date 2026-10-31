"""
LeetCode 16 - 3Sum Closest (Medium)

Problem: Given an integer array nums of length n and an integer target, find three integers in
nums (at different positions) such that their sum is closest to target. Return the sum of the
three integers. Each input has exactly one solution.
Constraints: 3 <= n <= 500, -1000 <= nums[i] <= 1000, -10^4 <= target <= 10^4.

Approach 1 - Brute force (threeSumClosestBruteForce):
    Key idea: try every triplet of positions i < j < k and keep the sum with the smallest
    distance |sum - target|.

    Complexity:
        Time:  O(n^3) -> C(n, 3) combinations.
        Space: O(1)

    Note: used as an oracle in the random tests.

Approach 2 - Sorting + fixed element + two pointers (threeSumClosest):
    Key idea: sort nums and fix i. The remaining problem is to find l, r to the right of i whose
    pair sum is as close as possible to new_target = target - nums[i]. Same pointer rule as in
    problem 15: pair sum too small -> l += 1, too large -> r -= 1, equal -> distance 0, return
    target directly. At every step, keep the triplet sum if it is CLOSER to target than the best
    one so far.
    Early exit: if nums[i] + nums[i + 1] + nums[i + 2] > target, that is the smallest sum of any
    triplet from i on (sorted array), so every other one is even further above target. The
    answer is the closer of that sum and the best one found before.

    Complexity:
        Time:  O(n^2) -> the outer loop runs n - 2 times and the two-pointer search at most
               n - i - 1 steps, since every step moves one pointer. Sorting is O(n log n),
               dominated by the O(n^2) search.
        Space: O(n) -> sorted() creates a copy of nums.

    Note:
        - We return the SUM, not the distance: store the best sum and compute the distance only
          to compare candidates.
        - "Closest" is not max(): compare candidates by abs(sum - target). min(a, b, key=f)
          returns whichever of a and b has the smallest f(value).
        - The function must return after the for loop: if no early exit happens, the loop just
          ends (otherwise it returns None).
        - No duplicate handling needed: we return a single number, not a list of triplets.
"""

import random


class Solution:
    def threeSumClosestBruteForce(self, nums: list[int], target: int) -> int:
        """Try every triplet and keep the sum closest to target."""
        n = len(nums)
        best_sum = nums[0] + nums[1] + nums[2]

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    current_sum = nums[i] + nums[j] + nums[k]
                    if abs(current_sum - target) < abs(best_sum - target):
                        best_sum = current_sum
        return best_sum

    def threeSumClosest(self, nums: list[int], target: int) -> int:
        """Sort nums, fix one element and find the other two with two pointers."""

        def distance(value: int) -> int:
            return abs(value - target)

        n = len(nums)
        nums = sorted(nums)
        best_sum = nums[0] + nums[1] + nums[2]

        for i in range(n - 2):
            smallest_sum = nums[i] + nums[i + 1] + nums[i + 2]
            if smallest_sum > target:
                # Every triplet from i on is >= smallest_sum > target: none can be closer
                return min(smallest_sum, best_sum, key=distance)

            new_target = target - nums[i]
            l, r = i + 1, n - 1
            while l < r:
                pair_sum = nums[l] + nums[r]
                if pair_sum == new_target:
                    return target  # distance 0: impossible to do better

                best_sum = min(nums[i] + pair_sum, best_sum, key=distance)
                if pair_sum < new_target:
                    l += 1  # sum too small -> increase it
                else:
                    r -= 1  # sum too large -> decrease it

        return best_sum


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([-1, 2, 1, -4], 1, 2),  # example 1: -1 + 2 + 1
        ([0, 0, 0], 1, 0),  # example 2: only one triplet
        ([1, 2, 3, 4, 5, 6, 7], -1, 6),  # early exit on the first i: 1 + 2 + 3
        ([0, 1, 1, 4, 5, 6, 7], -1, 2),  # 0 + 1 + 1
        ([1, 1, 1, 0], 100, 3),  # target far above every sum: 1 + 1 + 1
        ([-5, -4, -3, 10], -100, -12),  # target far below every sum
        ([4, 0, 5, -5, 3, 3, 0, -4, -5], -2, -2),  # exact match -> return target
        ([1, 1, -1, -1, 3], -1, -1),  # duplicates
        ([-100, -98, -2, -1], -101, -101),  # best triplet mixes far and near values
    ]

    for method in (sol.threeSumClosestBruteForce, sol.threeSumClosest):
        for nums, target, expected in test_cases:
            result = method(nums, target)
            assert result == expected, (method.__name__, nums, target, result)

        # Random tests: compare distances against the brute force
        # (two different sums can be equally close, so we compare distances, not sums)
        random.seed(0)
        for _ in range(500):
            nums = [random.randint(-20, 20) for _ in range(random.randint(3, 12))]
            target = random.randint(-60, 60)
            got = method(nums, target)
            best = sol.threeSumClosestBruteForce(nums, target)
            assert abs(got - target) == abs(best - target), (nums, target, got, best)

        print(f"{method.__name__}: OK")
