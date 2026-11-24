"""
LeetCode 36 - Valid Sudoku (Medium)

Problem:
    Determine if a 9 x 9 Sudoku board is valid. Only the filled cells need
    to be validated:
    1. Each row must contain the digits 1-9 without repetition.
    2. Each column must contain the digits 1-9 without repetition.
    3. Each of the nine 3 x 3 sub-boxes must contain the digits 1-9
       without repetition.
    Empty cells are represented by ".". A valid board is not necessarily
    solvable.

Approach 1 - Three passes (rows, columns, boxes)

    One helper per rule, each scanning the board with a fresh set per
    unit (row / column / box) and returning False on the first duplicate.
    The final verdict is rows() and columns() and boxes(), which
    short-circuits as soon as one rule fails.
    - Columns are obtained with zip(*board) (transpose).
    - Boxes are iterated from their top-left corners (r0, c0) in
      (0, 3, 6) x (0, 3, 6), then range(r0, r0 + 3) x range(c0, c0 + 3).

    Complexity (n x n board, here n = 9):
        Time:  O(n^2) -> each helper visits every cell once.
        Space: O(n)   -> one set of at most n elements alive at a time.

Approach 2 - Single pass with 27 sets

    Keep 9 sets for rows, 9 for columns and 9 for boxes. Visit each cell
    once and check it against its row, column and box at the same time.
    Box index of cell (r, c):

        box = (r // 3) * 3 + c // 3

    r // 3 is the box row (0-2), times 3 jumps to that row of boxes;
    c // 3 is the box column (0-2). E.g. (4, 7) -> 1 * 3 + 2 = 5.

    Complexity (n x n board, here n = 9):
        Time:  O(n^2) -> single pass over every cell.
        Space: O(n^2) -> 3n sets holding up to n elements each.

    Note:
        - The board is always 9 x 9, so strictly both approaches are
          O(1) in time and space (classic interview trick question).
        - {} is an empty dict, not a set: use set().
        - [set()] * 9 creates 9 references to the SAME set: use
          [set() for _ in range(9)].
        - Skip "." before checking, so empty cells never enter the sets.
        - Approach 2 is the one usually expected in interviews.
"""

import copy


class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        """Approach 2 - Single pass with 27 sets (submitted solution)."""
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for r in range(9):
            for c in range(9):
                elem = board[r][c]
                if elem == ".":
                    continue
                b = (r // 3) * 3 + c // 3  # box index 0-8
                if elem in rows[r] or elem in cols[c] or elem in boxes[b]:
                    return False
                rows[r].add(elem)
                cols[c].add(elem)
                boxes[b].add(elem)

        return True

    def is_valid_sudoku_three_passes(self, board: list[list[str]]) -> bool:
        """Approach 1 - Three passes (rows, columns, boxes)."""

        def rows_valid() -> bool:
            for row in board:
                seen = set()
                for elem in row:
                    if elem == ".":
                        continue
                    if elem in seen:
                        return False
                    seen.add(elem)
            return True

        def columns_valid() -> bool:
            for column in zip(*board):  # transpose: iterate columns
                seen = set()
                for elem in column:
                    if elem == ".":
                        continue
                    if elem in seen:
                        return False
                    seen.add(elem)
            return True

        def boxes_valid() -> bool:
            for r0 in (0, 3, 6):
                for c0 in (0, 3, 6):  # (r0, c0) = top-left corner of box
                    seen = set()
                    for r in range(r0, r0 + 3):
                        for c in range(c0, c0 + 3):
                            elem = board[r][c]
                            if elem == ".":
                                continue
                            if elem in seen:
                                return False
                            seen.add(elem)
            return True

        return rows_valid() and columns_valid() and boxes_valid()


def with_cell(board: list[list[str]], r: int, c: int, value: str) -> list[list[str]]:
    """Return a copy of board with board[r][c] = value."""
    new_board = copy.deepcopy(board)
    new_board[r][c] = value
    return new_board


if __name__ == "__main__":
    sol = Solution()

    VALID = [
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
    EMPTY = [["."] * 9 for _ in range(9)]

    cases = (
        ("valid board", VALID, True),
        ("empty board", EMPTY, True),
        ("LeetCode example 2", with_cell(VALID, 0, 0, "8"), False),
        ("row-only duplicate", with_cell(VALID, 0, 7, "5"), False),
        ("column-only duplicate", with_cell(VALID, 8, 0, "5"), False),
        ("box-only duplicate", with_cell(VALID, 0, 2, "9"), False),
    )

    for name, board, expected in cases:
        assert sol.isValidSudoku(board) == expected, f"approach 2: {name}"
        assert sol.is_valid_sudoku_three_passes(board) == expected, (
            f"approach 1: {name}"
        )

    print("OK")
