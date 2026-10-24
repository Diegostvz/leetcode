"""
0006. Zigzag Conversion — Medium
https://leetcode.com/problems/zigzag-conversion/
Pattern: simulation
Complexity: O(n) time, O(n) space
Notes:
- Simulate writing the string row by row: go down until the last row, then
  up until the first one, flipping the direction (step) at each edge.
- Edge case: with 1 row (or more rows than characters) the string does not
  change; returning early also avoids a step of 0.
- Alternative: compute each row's indices directly using the cycle length
  2 * (numRows - 1). Same complexity, less readable.
"""


class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [[] for _ in range(numRows)]
        row, step = 0, 1

        for char in s:
            rows[row].append(char)
            if row == 0:
                step = 1
            elif row == numRows - 1:
                step = -1
            row += step

        return "".join("".join(row) for row in rows)


if __name__ == "__main__":
    sol = Solution()
    assert sol.convert("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"
    assert sol.convert("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"
    assert sol.convert("A", 1) == "A"
    assert sol.convert("AB", 1) == "AB"
    print("OK")
