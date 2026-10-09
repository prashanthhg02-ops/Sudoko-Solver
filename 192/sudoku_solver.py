"""Solve a Sudoku puzzle using constraint search and backtracking."""

import argparse
import sys


SIZE = 9
BOX_SIZE = 3
FULL_MASK = (1 << SIZE) - 1


def parse_puzzle(puzzle: str) -> tuple[list[int], list[int], list[int], list[int]]:
    """Parse an 81-character puzzle, using 0 or . for empty cells."""
    if len(puzzle) != SIZE * SIZE:
        raise ValueError("Puzzle must contain exactly 81 characters.")

    board: list[int] = []
    row_masks = [0] * SIZE
    column_masks = [0] * SIZE
    box_masks = [0] * SIZE

    for index, char in enumerate(puzzle):
        if char in "0.":
            board.append(0)
            continue
        if char < "1" or char > "9":
            raise ValueError("Puzzle may contain only digits 1-9, 0, and .")

        value = int(char)
        bit = 1 << (value - 1)
        row = index // SIZE
        column = index % SIZE
        box = (row // BOX_SIZE) * BOX_SIZE + column // BOX_SIZE
        if (row_masks[row] | column_masks[column] | box_masks[box]) & bit:
            raise ValueError("Puzzle has duplicate digits in a row, column, or box.")

        board.append(value)
        row_masks[row] |= bit
        column_masks[column] |= bit
        box_masks[box] |= bit

    return board, row_masks, column_masks, box_masks


def solve(puzzle: str) -> str | None:
    """Return the solved puzzle as 81 digits, or None if it has no solution."""
    board, row_masks, column_masks, box_masks = parse_puzzle(puzzle)

    def search() -> bool:
        best_index = -1
        best_candidates = 0
        fewest_candidates = SIZE + 1

        for index, value in enumerate(board):
            if value:
                continue

            row = index // SIZE
            column = index % SIZE
            box = (row // BOX_SIZE) * BOX_SIZE + column // BOX_SIZE
            candidates = FULL_MASK & ~(
                row_masks[row] | column_masks[column] | box_masks[box]
            )
            candidate_count = candidates.bit_count()
            if candidate_count == 0:
                return False
            if candidate_count < fewest_candidates:
                best_index = index
                best_candidates = candidates
                fewest_candidates = candidate_count
                if candidate_count == 1:
                    break

        if best_index == -1:
            return True

        row = best_index // SIZE
        column = best_index % SIZE
        box = (row // BOX_SIZE) * BOX_SIZE + column // BOX_SIZE
        while best_candidates:
            bit = best_candidates & -best_candidates
            best_candidates &= best_candidates - 1
            board[best_index] = bit.bit_length()
            row_masks[row] |= bit
            column_masks[column] |= bit
            box_masks[box] |= bit

            if search():
                return True

            board[best_index] = 0
            row_masks[row] ^= bit
            column_masks[column] ^= bit
            box_masks[box] ^= bit

        return False

    if not search():
        return None
    return "".join(str(value) for value in board)


def format_grid(solution: str) -> str:
    """Format an 81-character solution as a readable 9-by-9 grid."""
    lines = []
    for row in range(SIZE):
        values = [solution[row * SIZE + column] for column in range(SIZE)]
        lines.append(
            " | ".join(
                " ".join(values[start : start + BOX_SIZE])
                for start in range(0, SIZE, BOX_SIZE)
            )
        )
        if row in (2, 5):
            lines.append("------+-------+------")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Solve a Sudoku puzzle with constraint search."
    )
    parser.add_argument(
        "puzzle",
        nargs="?",
        help="81 digits, using 0 or . for empty cells; omit to enter it at the prompt",
    )
    args = parser.parse_args()

    puzzle = args.puzzle
    if puzzle is None:
        puzzle = input("Enter 81 digits (use 0 or . for empty cells): ").strip()

    try:
        solution = solve(puzzle)
    except ValueError as error:
        parser.error(str(error))

    if solution is None:
        print("This Sudoku puzzle has no solution.", file=sys.stderr)
        return 1

    print(format_grid(solution))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
