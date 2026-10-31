"""
LeetCode 15 - 3Sum (Medium)

Problem: Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such
that i != j, i != k, j != k and nums[i] + nums[j] + nums[k] == 0. The solution set must not
contain duplicate triplets; the order of the output and of the triplets does not matter.
Constraints: 3 <= len(nums) <= 3000, -10^5 <= nums[i] <= 10^5.

Approach 1 - Brute force over every triplet of positions (threeSumBruteForce):
    Key idea: fix i, then j > i, then try every k > j. Since j always starts after i and k after
    j, each combination of positions is checked exactly once: every triplet involving elements
    to the left of i was already checked in a previous iteration of i.
    To avoid duplicates (e.g. two -1 in nums give [-1, 0, 1] twice), each valid triplet is
    normalized by sorting it and stored as a tuple in a set.

    Complexity:
        Time:  O(n^3) -> the loops run n - 2, n - i - 2 and n - j - 1 times, which gives
               C(n, 3) = n(n - 1)(n - 2) / 6 combinations. With n = 3000: ~4.5 * 10^9 -> TLE.
        Space: O(t) -> t = number of unique valid triplets stored in the set. In the worst case
               t is O(n^2): once two elements are chosen, the third one is fixed (-(a + b)).

    Note:
        - Same index bug as in problem 11: use absolute positions (range(i + 1, ...)) instead
          of offsets from the previous index.
        - "solutions = set" assigns the class itself; an empty set needs set().
        - Lists are unhashable and cannot go inside a set: convert each triplet to a tuple,
          and back to a list when returning.
        - The order of a set is arbitrary, so the tests sort the output before comparing.

Approach 2 - Sorting + fixed element + two pointers (threeSum):
    Key idea: sort nums. For each fixed i, the problem becomes 2Sum on a sorted array: find l, r
    to the right of i with nums[l] + nums[r] == -nums[i]. Start with l = i + 1, r = n - 1:
        - sum too small -> l += 1 (the only way to increase it in a sorted array)
        - sum too large -> r -= 1 (the only way to decrease it)
        - sum == target -> store the triplet and move BOTH pointers inwards
    Duplicates are skipped without a set, because equal values are adjacent after sorting:
        - if nums[i] == nums[i - 1], every triplet starting with it was already found -> skip
        - after a match, advance l while it points to the same value as before
    Early exit: if nums[i] > 0, every element from i on is positive, so no sum can be 0 -> break.

    Complexity:
        Time:  O(n^2) -> sorting is O(n log n), and for each of the n values of i the while loop
               runs at most n - i - 1 steps, because every step moves one pointer inwards.
               The gain is NOT in the outer loop (i still visits every position) but in the inner
               search: O(n) steps instead of O(n^2) pairs. Each pointer move discards a whole
               set of pairs at once: if the sum is too small with r, it is even smaller with any
               r' < r, so all pairs (l, r') are ruled out without checking them.
        Space: O(n) -> sorted() creates a copy of nums (plus the output, as in Approach 1).

    Note:
        - Pointer rule differs from problem 11: there we moved the SHORTER line; here the array
          is sorted, so nums[l] <= nums[r] always and the comparison between them is useless.
          What decides the move is the sum compared with the target.
        - After a match both pointers must move, otherwise the while loop never ends.
        - The loop that skips repeated values of l needs its own bound (l < r): with [0, 0, 0]
          it would otherwise run past the end of the array -> IndexError.
        - Use continue (not pass inside an if/elif/else chain) to skip an iteration: it avoids
          nesting the whole two-pointer search inside an else block.
        - The brute force acts as an oracle in the random tests below.
"""

import random


class Solution:
    def threeSumBruteForce(self, nums: list[int]) -> list[list[int]]:
        """Check every combination of three positions and keep the unique valid triplets."""
        n = len(nums)
        solutions = set()

        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    if nums[i] + nums[j] + nums[k] == 0:
                        # Sorting normalizes the triplet so duplicates look identical
                        triplet = tuple(sorted((nums[i], nums[j], nums[k])))
                        solutions.add(triplet)

        return [list(triplet) for triplet in solutions]

    def threeSum(self, nums: list[int]) -> list[list[int]]:
        """Sort nums, fix one element and find the other two with two pointers."""
        n = len(nums)
        solutions = []
        nums = sorted(nums)

        for i in range(n - 2):
            smallest_num = nums[i]
            if smallest_num > 0:
                break  # everything from here on is positive: no sum can be 0
            if i > 0 and smallest_num == nums[i - 1]:
                continue  # same value as the previous i: its triplets are already found

            target = -smallest_num
            l, r = i + 1, n - 1
            while l < r:
                pair_sum = nums[l] + nums[r]
                if pair_sum == target:
                    solutions.append([smallest_num, nums[l], nums[r]])
                    old_value = nums[l]
                    # Skip repeated values of l; l < r keeps the index inside the array
                    while l < r and nums[l] == old_value:
                        l += 1
                    r -= 1
                elif pair_sum < target:
                    l += 1  # sum too small -> increase it
                else:
                    r -= 1  # sum too large -> decrease it
        return solutions


def normalize(triplets: list[list[int]]) -> list[list[int]]:
    """Sort each triplet and the list of triplets, so the order does not affect the tests."""
    return sorted(sorted(triplet) for triplet in triplets)


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([0, 0, 0], [[0, 0, 0]]),
        ([0, 1, 1], []),  # no valid triplet
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),  # duplicate -1 in the input
        ([0, 0, 0, 0], [[0, 0, 0]]),  # many duplicates -> a single triplet
        ([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]]),
        ([1, 2, -2, -1], []),
        (
            [-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],
            [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]],
        ),  # many duplicates on both sides
    ]

    for method in (sol.threeSumBruteForce, sol.threeSum):
        for nums, expected in test_cases:
            assert normalize(method(nums)) == normalize(expected), (
                method.__name__,
                nums,
            )

        # Random tests: compare against the brute force on small inputs
        random.seed(0)
        for _ in range(200):
            nums = [random.randint(-5, 5) for _ in range(random.randint(3, 12))]
            assert normalize(method(nums)) == normalize(sol.threeSumBruteForce(nums)), (
                nums
            )

        print(f"{method.__name__}: OK")
