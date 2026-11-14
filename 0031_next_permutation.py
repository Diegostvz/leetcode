"""
LeetCode 31 - Next Permutation (Medium)

Problem: The next permutation of an array of integers is the next one in lexicographic order
(think of the array as the digits of a number: the next bigger number with the same digits).
If it is the last permutation (sorted in descending order), the next one is the first
(sorted in ascending order). Modify nums IN PLACE using only constant extra memory.
E.g. [1, 2, 3] -> [1, 3, 2], [3, 2, 1] -> [1, 2, 3], [1, 1, 5] -> [1, 5, 1].
(1 <= len(nums) <= 100, 0 <= nums[i] <= 100)

Approach 1 - Pivot, swap with the next bigger, reverse the suffix (nextPermutation):
    Key idea: the longest suffix sorted in DESCENDING order is already the biggest possible
    arrangement of its elements, so it cannot grow without touching the element before it.
        1. Pivot: scanning from the right, the first index p with nums[p] < nums[p + 1].
           If there is none, the whole array is descending (last permutation): reverse it.
        2. Swap the pivot with the smallest element of the suffix that is BIGGER than it.
           The suffix is descending, so it is the first one found scanning from the end.
        3. The suffix is still descending: reverse it to make it as small as possible.

        [1, 2, 4, 3, 1]: pivot 2 (index 1), suffix [4, 3, 1]
        swap 2 with 3 (smallest bigger than 2) -> [1, 3, 4, 2, 1]
        reverse the suffix [4, 2, 1]           -> [1, 3, 1, 2, 4]

    Complexity (n = len(nums)):
        Time:  O(n) -> at most three linear scans: find the pivot, find j, reverse.
        Space: O(1) -> swaps and a two-pointer reversal, all in place.

    Note:
        - Strict < for the pivot: equal neighbours cannot be improved ([5, 1, 1] -> [1, 1, 5]).
        - <= when searching j: with duplicates it picks the RIGHTMOST bigger element, which
          keeps the suffix descending after the swap, so reversing it sorts it.
        - The element to swap is the smallest BIGGER than the pivot, not the smallest of the
          suffix: [2, 3, 1] must give [3, 1, 2], not [1, 3, 2] (that would go backwards).
        - In place: nums[i] = ..., swaps, nums[:] = ... and nums.reverse() modify the list;
          nums = ... only rebinds the local name. nums.reverse() is O(1) extra memory,
          nums[:] = nums[::-1] builds a temporary copy first.
        - nums[a:].reverse() reverses a COPY and returns None: reverse a slice in place with
          two pointers (swap and move them towards each other).
"""


class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums) - 1, 0, -1):  # scan pairs (i - 1, i) from the right
            pivot = i - 1
            if nums[pivot] < nums[i]:  # 1. first break of the descending suffix
                # 2. smallest element bigger than the pivot = first one from the end
                j = len(nums) - 1
                while (
                    nums[j] <= nums[pivot]
                ):  # skip everything not bigger than the pivot
                    j -= 1
                nums[pivot], nums[j] = nums[j], nums[pivot]

                # 3. reverse the suffix in place (it is still descending)
                left, right = pivot + 1, len(nums) - 1
                while left < right:
                    nums[left], nums[right] = nums[right], nums[left]
                    left += 1
                    right -= 1
                break
        else:  # no pivot: last permutation -> first
            nums.reverse()


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 2, 3], [1, 3, 2]),
        ([3, 2, 1], [1, 2, 3]),  # last permutation -> first
        ([1, 1, 5], [1, 5, 1]),  # duplicates
        ([1, 3, 2], [2, 1, 3]),
        ([2, 3, 1], [3, 1, 2]),  # smallest BIGGER, not smallest
        ([1], [1]),  # single element
        ([1, 5, 1], [5, 1, 1]),
        ([5, 1, 1], [1, 1, 5]),  # equal neighbours are not a pivot
        ([2, 1, 3], [2, 3, 1]),  # only the last two change
        ([1, 2, 4, 3, 1], [1, 3, 1, 2, 4]),
    ]

    for values, expected in test_cases:
        nums = values.copy()
        sol.nextPermutation(nums)  # modifies nums in place, returns None
        assert nums == expected, (values, nums)

    # Brute force: applying it repeatedly must walk through every permutation in order
    from itertools import permutations

    for start in ([1, 2, 3, 4], [1, 1, 2, 2], [0, 1, 2, 3, 4]):
        expected_order = sorted(set(permutations(start)))
        nums = start.copy()
        for perm in expected_order[1:] + expected_order[:1]:  # wraps around at the end
            sol.nextPermutation(nums)
            assert tuple(nums) == perm, (start, nums, perm)

    print("OK")
