# Sudoku Solver

A dependency-free Python Sudoku solver using constraint search and
backtracking. It applies the minimum-remaining-values heuristic by trying the
empty cell with the fewest legal digits first.

## Run

Pass a puzzle as 81 characters in row order. Use `0` or `.` for empty cells:

```powershell
python sudoku_solver.py 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

You can also run the program without an argument and enter the puzzle when
prompted:

```powershell
python sudoku_solver.py
```

The solver prints the completed grid. It reports malformed puzzles and
duplicate clues as input errors, and reports when a valid puzzle has no
solution.

## Tests

Run the built-in tests with:

```powershell
python -m unittest -v
```
