"""
LeetCode 26 - Remove Duplicates from Sorted Array (Easy)

Problem: Given an integer array nums sorted in non-decreasing order, remove the duplicates
IN PLACE so that each unique element appears only once, keeping their relative order.
Return k, the number of unique elements: the first k elements of nums must hold them; what
is left beyond position k does not matter.
(1 <= len(nums) <= 3 * 10^4, -100 <= nums[i] <= 100)

Approach 1 - Pop every duplicate (removeDuplicatesPop):
    Key idea: walk the array comparing each element with the previous one; if they are equal,
    pop it. Since every pop shifts the rest one position to the left, the index is corrected
    by the number of elements already popped.

    Complexity (n = len(nums)):
        Time:  O(n^2) -> pop(i) is O(n), not O(1): every element after i is shifted left.
               Worst case, all equal ([7, 7, ..., 7]): n - 1 pops of up to n shifts each.
        Space: O(1) -> in place.

    Note:
        - Only pop() at the END of a list is O(1); pop(i) in the middle is O(n).

Approach 2 - Two pointers: read with fast, write with slow (removeDuplicates):
    Key idea: nothing needs to be deleted, only overwritten. slow marks the last unique value
    written (nums[0] is always unique); fast reads every element. When nums[fast] differs from
    nums[slow], it is a new unique value: write it right after slow and advance slow.
    Duplicates are simply skipped. At the end, the uniques are nums[0 .. slow], so k = slow + 1.

        nums = [1, 1, 2, 3, 3]
        fast = 2 -> 2 != 1 -> nums[1] = 2 -> [1, 2, 2, 3, 3], slow = 1
        fast = 3 -> 3 != 2 -> nums[2] = 3 -> [1, 2, 3, 3, 3], slow = 2  -> k = 3

    Complexity (n = len(nums)):
        Time:  O(n) -> one pass, O(1) work per element (comparison + assignment).
        Space: O(1) -> two indices, in place.

    Note:
        - Optimal: every element must be read at least once.
        - Comparing with nums[slow] (the last unique written) works because the array is
          sorted: all duplicates of a value are contiguous.
        - Same read/write two-pointer pattern as LeetCode 27 (Remove Element) and 283
          (Move Zeroes).
"""


class Solution:
    def removeDuplicatesPop(self, nums: list[int]) -> int:
        """Pop each element equal to the previous one, correcting the index after each pop."""
        popped = 0
        for idx in range(1, len(nums)):
            adapted_idx = idx - popped  # position of the original idx after the pops
            if nums[adapted_idx - 1] == nums[adapted_idx]:
                nums.pop(adapted_idx)
                popped += 1
        return len(nums)

    def removeDuplicates(self, nums: list[int]) -> int:
        """Overwrite in place: fast reads every element, slow marks the last unique written."""
        slow = 0  # nums[0] is always unique
        for fast in range(1, len(nums)):
            if nums[fast] != nums[slow]:  # new unique value
                slow += 1
                nums[slow] = nums[fast]
        return slow + 1  # uniques are nums[0 .. slow]


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1], [1]),  # single element
        ([1, 2, 3], [1, 2, 3]),  # no duplicates
        ([1, 1, 2], [1, 2]),
        ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], [0, 1, 2, 3, 4]),
        ([1, 2, 3, 4, 4, 4, 4, 5], [1, 2, 3, 4, 5]),
        ([7, 7, 7, 7], [7]),  # all equal: worst case for pop
        ([-3, -3, -1, 0, 0, 5], [-3, -1, 0, 5]),  # negatives
        ([1, 2, 2], [1, 2]),  # duplicates at the end
        (
            sorted([v % 201 - 100 for v in range(30000)]),
            list(range(-100, 101)),
        ),  # max size
    ]

    for method in (sol.removeDuplicatesPop, sol.removeDuplicates):
        for values, expected in test_cases:
            nums = values.copy()  # the method modifies nums in place
            k = method(nums)
            assert k == len(expected) and nums[:k] == expected, (
                method.__name__,
                values[:10],
                k,
            )
        print(f"{method.__name__}: OK")
