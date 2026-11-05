"""
LeetCode 20 - Valid Parentheses (Easy)

Problem: Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid. A string is valid if:
    1. Open brackets are closed by the same type of brackets.
    2. Open brackets are closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.
(1 <= len(s) <= 10^4)

Approach 1 - Stack of opening brackets (isValid):
    Key idea: the last bracket opened must be the first one closed, which is exactly how a
    stack works (LIFO: last in, first out), emulated with a Python list (append / pop).
    Push every opening bracket. For every closing bracket, pop the last opener and check that
    they match; if the stack is empty or they do not match, the string is invalid.
    At the end, the string is valid only if the stack is empty (no opener left unclosed).

    Complexity (L = len(s)):
        Time:  O(L) -> one pass, O(1) work per character (dict lookup, append, pop).
        Space: O(L) -> in the worst case every character is an opener, e.g. "((((((".
                       The dict has a fixed size, so it does not count.

    Note:
        - Optimal: every character must be read at least once, so O(L) time is a lower bound.
        - Early exit: if len(s) is odd, the brackets cannot be paired -> return False.
        - Three ways to fail: a closer with an empty stack (")"), a closer that does not match
          the last opener ("(]"), or openers left in the stack at the end ("((").
        - Python lists are efficient stacks: append and pop at the end are O(1).
"""


class Solution:
    def isValid(self, s: str) -> bool:
        """Push openers onto a stack and match each closer with the last opener."""
        if len(s) % 2:  # odd length: some bracket cannot have a pair
            return False

        pairs = {"(": ")", "[": "]", "{": "}"}  # opener -> closer
        stack = []

        for char in s:
            if char in pairs:  # opening bracket
                stack.append(char)
            elif not stack or pairs[stack.pop()] != char:  # closing bracket
                return False

        return not stack  # valid only if every opener was closed


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("()", True),
        ("[]", True),
        ("{}", True),
        ("()[]{}", True),
        ("[()]", True),
        ("{[()()]}", True),  # deep nesting
        ("", True),  # empty string (outside the constraints, but valid)
        ("(]", False),  # wrong type
        ("([)]", False),  # wrong order
        ("([{)])", False),
        ("((", False),  # openers left unclosed
        (")", False),  # closer with an empty stack
        ("())", False),  # extra closer
        ("(((", False),  # odd length
        ("(" * 5000 + ")" * 5000, True),  # max length
    ]

    for s, expected in test_cases:
        assert sol.isValid(s) == expected, s
    print("OK")
