"""
LeetCode 32 - Longest Valid Parentheses (Hard)

Problem: Given a string s containing just the characters '(' and ')', return the length of
the longest CONTIGUOUS substring that is a valid (well-formed) parentheses string.
(0 <= len(s) <= 3 * 10^4)

Approach 1 - Stack of indices with a "wall" at the bottom (longestValidParentheses):
    Key idea: counting matched pairs is not enough, because pairs separated by an unmatched
    character do not form one valid substring: in "()(()" there are 2 pairs but the answer
    is 2, not 4. Store INDICES in the stack instead of characters:
        - at the bottom, always a wall: the index of the last character that cannot belong to
          any valid substring (a fake wall at -1 at the start, then every unmatched ")");
        - above it, the indices of the "(" still waiting for a pair.
    Rules:
        1. "(" -> push its index.
        2. ")" -> pop. If the stack is not empty, the top is the last unmatched position, so the
           valid substring ending at idx has length idx - stack[-1]: update the maximum.
           If it is empty, the wall was popped: this ")" has no pair and becomes the new wall.

        ")()())":  [-1] -> ")" pop, empty -> wall 0 -> [0]
                   "(" -> [0, 1]   ")" -> [0], 2 - 0 = 2
                   "(" -> [0, 3]   ")" -> [0], 4 - 0 = 4   <- adjacent blocks join
                   ")" pop, empty -> wall 5 -> [5]                          answer: 4

    Complexity (n = len(s)):
        Time:  O(n) -> one pass, O(1) work per character (push / pop / subtraction).
        Space: O(n) -> worst case every character is an unclosed "(", e.g. "((((((".

    Note:
        - Pop FIRST, then check whether the stack is empty: thanks to the wall it is never
          empty before the pop.
        - Keep the MAXIMUM with max(); a plain assignment keeps only the last length.
        - Unclosed "(" left in the stack act as walls too: in "()(()" the last subtraction is
          against index 2, not against -1.
        - Same stack idea as LeetCode 20 (Valid Parentheses), but storing positions.
        - O(1) space alternative: two passes counting opened / closed (left to right, then
          right to left), resetting when the counts become invalid.
"""


class Solution:
    def longestValidParentheses(self, s: str) -> int:
        """Track the last unmatched position at the bottom of a stack of indices."""
        stack = [-1]  # fake wall: position right before the string
        longest = 0

        for idx, char in enumerate(s):
            if char == "(":
                stack.append(idx)  # waiting for a pair
            else:  # ")"
                stack.pop()
                if stack:  # something left below: a wall or an open "("
                    longest = max(longest, idx - stack[-1])
                else:  # we popped the wall: this ")" has no pair -> new wall
                    stack.append(idx)
        return longest


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("(()", 2),
        (")()())", 4),
        ("", 0),
        ("()(()", 2),  # unmatched "(" in the middle splits the pairs
        ("()(())", 6),  # adjacent valid blocks join
        ("(()())", 6),  # nested
        ("))((", 0),  # nothing valid
        ("()", 2),
        (")(", 0),
        ("()(()))())", 6),
        ("(())()((", 6),  # the longest is NOT the last one found
    ]

    for s, expected in test_cases:
        result = sol.longestValidParentheses(s)
        assert result == expected, (s, result)

    # Brute force: check every substring with a counter, on random small strings
    import random

    def is_valid(sub: str) -> bool:
        balance = 0
        for c in sub:
            balance += 1 if c == "(" else -1
            if balance < 0:
                return False
        return balance == 0

    for _ in range(2000):
        s = "".join(random.choices("()", k=random.randint(0, 14)))
        brute = max(
            (
                j - i
                for i in range(len(s) + 1)
                for j in range(i, len(s) + 1)
                if is_valid(s[i:j])
            ),
            default=0,
        )
        assert sol.longestValidParentheses(s) == brute, (s, brute)

    print("OK")
