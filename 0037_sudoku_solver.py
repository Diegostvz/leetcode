"""
LeetCode 37 - Sudoku Solver (Hard)

Problem:
    Solve a 9 x 9 Sudoku puzzle by filling the empty cells (".") in-place.
    A solution must satisfy:
    1. Each row contains the digits 1-9 exactly once.
    2. Each column contains the digits 1-9 exactly once.
    3. Each of the nine 3 x 3 sub-boxes contains the digits 1-9 exactly
       once.
    The input is guaranteed to have exactly one solution.

Approach 1 - Backtracking with 27 sets

    Reuse the 27 sets from LeetCode 36 (9 rows, 9 columns, 9 boxes) to
    check in O(1) whether a digit fits in a cell.
    1. Fill the sets with the initial digits and collect the empty cells.
    2. backtrack(i) fills empty[i]: try each digit 1-9 that is not in its
       row, column or box, place it (board + 3 sets) and recurse on i + 1.
    3. If the recursion fails, undo the digit (board + 3 sets) and try the
       next one. If no digit fits, return False to go back one cell.
    4. When i == len(empty), every cell is filled -> solved.

    Box index of cell (r, c):

        box = (r // 3) * 3 + c // 3

    Complexity (k = number of empty cells):
        Time:  O(9^k) worst case -> up to 9 options per empty cell.
               Bounded since the board is 9 x 9 (k <= 81), so O(1) in
               strict terms, but exponential in nature.
        Space: O(k) recursion depth + 27 sets of at most 9 elements.

    Note:
        - backtrack returns bool so that, once solved, the recursion stops
          and does NOT undo the solution on the way back.
        - Place and undo must be symmetric: board + rows + cols + boxes.
        - d not in (set1, set2, set3) checks if d EQUALS one of the sets,
          not if it is inside them. Use d not in s1 and d not in s2 ...
        - No need to validate the input: it is guaranteed to be solvable.
        - The board is modified in-place; the method returns None.
"""


class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:

        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]
        empty = []  # list of (r, c) empty cells

        # 1. Fill the sets with the initial digits and collect the empty cells
        for r in range(9):
            for c in range(9):
                elem = board[r][c]
                if elem == ".":
                    empty.append((r, c))
                    continue
                b = (r // 3) * 3 + c // 3  # box index 0-8
                rows[r].add(elem)
                cols[c].add(elem)
                boxes[b].add(elem)

        def backtrack(i: int) -> bool:
            if i == len(empty):
                return True  # all cells filled
            r, c = empty[i]
            b = (r // 3) * 3 + c // 3
            for d in "123456789":
                if d not in rows[r] and d not in cols[c] and d not in boxes[b]:
                    # place d (board + 3 sets)
                    board[r][c] = d
                    rows[r].add(d)
                    cols[c].add(d)
                    boxes[b].add(d)

                    if backtrack(i + 1):
                        return True

                    # undo d (board + 3 sets)
                    board[r][c] = "."
                    rows[r].remove(d)
                    cols[c].remove(d)
                    boxes[b].remove(d)
            return False  # no digit fits -> go back

        backtrack(0)


def is_solved(board: list[list[str]]) -> bool:
    """Check that board is full and every row, column and box has 1-9."""
    digits = set("123456789")
    rows_ok = all(set(row) == digits for row in board)
    cols_ok = all(set(col) == digits for col in zip(*board))
    boxes_ok = all(
        {board[r][c] for r in range(r0, r0 + 3) for c in range(c0, c0 + 3)} == digits
        for r0 in (0, 3, 6)
        for c0 in (0, 3, 6)
    )
    return rows_ok and cols_ok and boxes_ok


if __name__ == "__main__":
    sol = Solution()

    # LeetCode example: known unique solution
    board = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    expected = [
        "534678912",
        "672195348",
        "198342567",
        "859761423",
        "426853791",
        "713924856",
        "961537284",
        "287419635",
        "345286179",
    ]
    assert sol.solveSudoku(board) is None  # in-place, returns None
    assert ["".join(row) for row in board] == expected
    assert is_solved(board)

    # Empty board: any valid full grid is accepted
    empty = [["."] * 9 for _ in range(9)]
    sol.solveSudoku(empty)
    assert is_solved(empty)

    # Already solved board: must stay unchanged
    solved = [list(row) for row in expected]
    sol.solveSudoku(solved)
    assert ["".join(row) for row in solved] == expected

    print("OK")
