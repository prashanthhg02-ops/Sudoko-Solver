import unittest

from sudoku_solver import format_grid, parse_puzzle, solve


PUZZLE = (
    "530070000"
    "600195000"
    "098000060"
    "800060003"
    "400803001"
    "700020006"
    "060000280"
    "000419005"
    "000080079"
)
SOLUTION = (
    "534678912"
    "672195348"
    "198342567"
    "859761423"
    "426853791"
    "713924856"
    "961537284"
    "287419635"
    "345286179"
)


class SudokuSolverTests(unittest.TestCase):
    def test_solves_puzzle(self) -> None:
        self.assertEqual(solve(PUZZLE), SOLUTION)

    def test_returns_none_for_unsolvable_puzzle(self) -> None:
        puzzle = (
            "531070000"
            "600195000"
            "098000060"
            "800060003"
            "400803001"
            "700020006"
            "060000280"
            "000419005"
            "000080079"
        )
        self.assertIsNone(solve(puzzle))

    def test_solution_preserves_clues(self) -> None:
        solution = solve(PUZZLE)
        self.assertIsNotNone(solution)
        for clue, solved in zip(PUZZLE, solution):
            if clue not in "0.":
                self.assertEqual(clue, solved)

    def test_rejects_wrong_length(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly 81"):
            solve("0" * 80)

    def test_rejects_invalid_character(self) -> None:
        with self.assertRaisesRegex(ValueError, "only digits"):
            solve("x" + "0" * 80)

    def test_rejects_duplicate_clues(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate digits"):
            solve("11" + "0" * 79)

    def test_formats_solution_as_grid(self) -> None:
        grid = format_grid(SOLUTION)
        self.assertEqual(len(grid.splitlines()), 11)
        self.assertEqual(grid.splitlines()[0], "5 3 4 | 6 7 8 | 9 1 2")
        self.assertEqual(grid.splitlines()[3], "------+-------+------")

    def test_parses_empty_cells(self) -> None:
        board, rows, columns, boxes = parse_puzzle("0" * 81)
        self.assertEqual(board, [0] * 81)
        self.assertEqual(rows, [0] * 9)
        self.assertEqual(columns, [0] * 9)
        self.assertEqual(boxes, [0] * 9)


if __name__ == "__main__":
    unittest.main()
