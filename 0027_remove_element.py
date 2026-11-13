"""
LeetCode 27 - Remove Element (Easy)

Problem: Given an integer array nums and an integer val, remove all occurrences of val IN
PLACE. The order of the remaining elements may change. Return k, the number of elements not
equal to val: the first k elements of nums must hold them; what is left beyond position k
does not matter.
(0 <= len(nums) <= 100, 0 <= nums[i] <= 50, 0 <= val <= 100)

Approach 1 - Delete every occurrence (removeElementDel):
    Key idea: walk the array and delete each element equal to val. Every deletion shifts the
    rest one position to the left, so the index is corrected by the number of elements already
    deleted. k is the original length minus the deleted ones.

    Complexity (n = len(nums)):
        Time:  O(n^2) -> del nums[i] is O(n): every element after i is shifted left.
               Worst case, all equal to val: n deletions of up to n shifts each.
        Space: O(1) -> in place.

    Note:
        - Sorting is NOT allowed as a shortcut: nums = sorted(nums) creates a NEW list bound to
          the local name nums, so the caller's list is never modified.

Approach 2 - Two pointers: read with fast, write with slow (removeElement):
    Key idea: nothing needs to be deleted, only overwritten. slow is the position where the
    NEXT kept element will be written (0 at the start: nothing written yet); fast reads every
    element. If nums[fast] != val, copy it to nums[slow] and advance slow. At the end, slow is
    exactly the number of elements written, so k = slow.

        nums = [3, 2, 2, 3], val = 3
        fast = 0 -> 3 == val -> skip
        fast = 1 -> 2 -> nums[0] = 2, slow = 1
        fast = 2 -> 2 -> nums[1] = 2, slow = 2
        fast = 3 -> 3 == val -> skip            -> k = 2, nums[:2] = [2, 2]

    Complexity (n = len(nums)):
        Time:  O(n) -> one pass, O(1) work per element.
        Space: O(1) -> two indices, in place.

    Note:
        - Optimal: every element must be read at least once.
        - Two conventions for slow; pick one and be consistent:
            * LeetCode 26: slow = position of the LAST element written (nums[0] is always kept)
              -> slow += 1, then nums[slow] = ...; return slow + 1.
            * LeetCode 27: slow = position of the NEXT element to write (nums[0] may be val)
              -> nums[slow] = ..., then slow += 1; return slow.
        - fast must start at 0 here: starting at 1 never reads nums[0] and overwrites it.
        - Empty input needs no special case: the loop does not run and 0 is returned.
"""


class Solution:
    def removeElementDel(self, nums: list[int], val: int) -> int:
        """Delete each occurrence of val, correcting the index after each deletion."""
        n = len(nums)
        deleted = 0
        for i in range(n):
            idx = i - deleted  # position of the original i after the deletions
            if nums[idx] == val:
                del nums[idx]
                deleted += 1
        return n - deleted

    def removeElement(self, nums: list[int], val: int) -> int:
        """Overwrite in place: fast reads every element, slow is where the next kept one goes."""
        slow = 0  # nothing written yet
        for fast in range(len(nums)):
            if nums[fast] != val:  # keep it
                nums[slow] = nums[fast]
                slow += 1
        return slow  # number of elements kept


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([3, 2, 2, 3], 3, [2, 2]),
        ([0, 1, 2, 2, 3, 0, 4, 2], 2, [0, 1, 3, 0, 4]),
        ([], 0, []),  # empty
        ([1], 1, []),  # remove everything
        ([4, 5], 3, [4, 5]),  # nothing to remove
        ([2, 2, 2], 2, []),  # all equal to val
        ([1, 2, 3, 1], 1, [2, 3]),  # val at both ends
        ([5, 2, 2, 4, 4, 3, 6], 4, [5, 2, 2, 3, 6]),
        (
            [v % 51 for v in range(100)],
            7,
            [v % 51 for v in range(100) if v % 51 != 7],
        ),  # max size
    ]

    for method in (sol.removeElementDel, sol.removeElement):
        for values, val, expected in test_cases:
            nums = values.copy()  # the method modifies nums in place
            k = method(nums, val)
            assert k == len(expected) and sorted(nums[:k]) == sorted(expected), (
                method.__name__,
                values,
                val,
                nums,
            )
        print(f"{method.__name__}: OK")
