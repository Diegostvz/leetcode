"""
0001. Two Sum — Easy
https://leetcode.com/problems/two-sum/
Pattern: hash map / complement lookup
Complexity: O(n) time, O(n) space
Notes:
- First approach: brute force, checking every pair with two nested loops.
  O(n^2) time, O(1) space.
- Final approach: one pass with a dict {value: index}. For each number, check
  whether its complement (target - x) has already been seen.
- Checking the complement BEFORE inserting the current number prevents using
  the same element twice (e.g. nums = [3], target = 6).
"""


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}  # value -> index
        for i, x in enumerate(nums):
            complement = target - x
            if complement in seen:
                return [seen[complement], i]
            seen[x] = i
        return []  # unreachable: the problem guarantees exactly one solution


if __name__ == "__main__":
    sol = Solution()
    assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert sol.twoSum([3, 2, 4], 6) == [1, 2]
    assert sol.twoSum([3, 3], 6) == [0, 1]
    print("OK")
