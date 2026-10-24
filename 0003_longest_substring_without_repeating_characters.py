"""
0003. Longest Substring Without Repeating Characters — Medium
https://leetcode.com/problems/longest-substring-without-repeating-characters/
Pattern: sliding window / hash set
Complexity: O(n) time, O(min(n, k)) space (k = alphabet size)
Notes:
- Window s[left:right+1] always contains unique characters.
- Each character enters and leaves the set at most once, so the inner while
  loop is O(n) in total, not per iteration: overall O(n).
- Alternative: dict {char: last index} lets `left` jump directly past the
  repeated character instead of shrinking one step at a time. Same complexity.
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()  # characters in the current window s[left:right+1]
        left = 0  # start index of the current window
        max_len = 0  # longest valid window found so far

        for right, char in enumerate(s):
            # Shrink the window from the left until char is no longer repeated
            while char in seen:
                seen.remove(s[left])
                left += 1

            # Now char can safely join the window
            seen.add(char)

            # Update the best length with the current window size
            max_len = max(max_len, right - left + 1)

        return max_len


if __name__ == "__main__":
    sol = Solution()
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    assert sol.lengthOfLongestSubstring("pwwkew") == 3
    assert sol.lengthOfLongestSubstring("") == 0
    print("OK")
