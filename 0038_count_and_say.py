"""
LeetCode 38 - Count and Say (Medium)

Problem:
    The count-and-say sequence is defined recursively:
    - countAndSay(1) = "1"
    - countAndSay(n) is the run-length encoding of countAndSay(n - 1):
      read the previous term aloud, group by group of equal consecutive
      digits, writing "<count><digit>" for each group.
    E.g. "1" -> "11" -> "21" -> "1211" -> "111221" -> "312211".
    Return the n-th term (1 <= n <= 30).

Approach 1 - Recursion + run-length encoding

    1. Base case: n == 1 -> "1".
    2. Get the previous term: prev = countAndSay(n - 1).
    3. Scan prev counting equal consecutive digits. When the digit
       changes, write the finished group (count + prev[i - 1]) and reset
       count to 1.
    4. After the loop, write the last group (it never sees a change).

    Complexity (L = length of the longest term):
        Time:  O(n * L) -> each of the n terms is scanned once.
               L grows ~30% per step (Conway's constant ~1.303), so it is
               exponential in n.
        Space: O(L) for the strings + O(n) recursion depth.

    Note:
        - n is the index of the term, NOT the string to describe: describe
          countAndSay(n - 1), not n.
        - On a change, write the group that ENDS (prev[i - 1]), not the
          one that starts (prev[i]).
        - The last group must be written after the loop.
        - count starts at 1: the first digit already counts.
        - Build with a list + "".join(): str += creates a new string
          every time..
"""


class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return "1"

        prev = self.countAndSay(n - 1)
        result = []
        count = 1
        for i in range(1, len(prev)):
            if prev[i] == prev[i - 1]:
                count += 1
            else:
                result.append(f"{count}{prev[i - 1]}")  # finished group
                count = 1
        result.append(f"{count}{prev[-1]}")  # last group

        return "".join(result)


if __name__ == "__main__":
    sol = Solution()

    sequence = ["1", "11", "21", "1211", "111221", "312211", "13112221"]
    for n, expected in enumerate(sequence, start=1):
        assert sol.countAndSay(n) == expected, f"n = {n}"

    assert len(sol.countAndSay(30)) == 4462  # max constraint

    print("OK")
