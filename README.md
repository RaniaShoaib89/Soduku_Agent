# CSP-Based Sudoku Solver

A constraint satisfaction problem (CSP) solver for Sudoku puzzles using **Backtracking Search**, **Forward Checking**, and **Arc Consistency (AC-3)** algorithm.

## Overview

This project implements an intelligent Sudoku solver that treats the puzzle as a CSP with:
- **Variables**: 81 cells in a 9×9 grid
- **Domain**: Each cell can contain digits 1-9 (0 represents empty cells)
- **Constraints**: 
  - Row constraints (each row has unique digits 1-9)
  - Column constraints (each column has unique digits 1-9)
  - 3×3 box constraints (each box has unique digits 1-9)

## Algorithm Details

### 1. **Backtracking Search**
- Systematically explores the solution space
- Assigns values to variables one at a time
- Backtracks when a constraint violation is detected
- Uses **Minimum Remaining Values (MRV)** heuristic for variable selection

### 2. **Forward Checking**
- Applied after each variable assignment
- Removes values from neighbor domains that conflict with the assignment
- Detects domain wipe-out (domain becomes empty) early
- Prunes the search tree significantly

### 3. **AC-3 Algorithm**
- Arc consistency algorithm for constraint propagation
- Applied initially and after each backtrack step
- Removes values from variable domains that have no consistent assignment
- Reduces search space by eliminating impossible values

### 4. **Heuristics**
- **MRV (Minimum Remaining Values)**: Select variable with smallest remaining domain
- **Domain Reduction**: AC-3 keeps domains as small as possible

## Structure

```
sudoku-csp/
├── sudoku_csp.py           # Core CSP solver implementation
├── solve_sudoku.py         # Main solver runner with report generation
├── easy.txt                # Easy Sudoku puzzle
├── medium.txt              # Medium difficulty puzzle
├── hard.txt                # Hard difficulty puzzle
├── veryhard.txt            # Very hard difficulty puzzle
├── validate_puzzles.py     # Puzzle validation utility
├── find_conflicts.py       # Conflict detection utility
├── sudoku_report.txt       # Generated results report
└── README.md               # This file
```

## Features

### Core Solver Features
- ✓ Full CSP formulation with constraint graph
- ✓ Backtracking with intelligent variable selection (MRV)
- ✓ Forward checking with domain wipe-out detection
- ✓ AC-3 constraint propagation
- ✓ Statistics tracking (backtrack calls and failures)
- ✓ Support for puzzles of varying difficulty

### Utilities
- Puzzle validation (detects invalid/duplicate values)
- Conflict detection tools
- Performance measurement
- Comprehensive reporting

## Usage

### Solving Puzzles

```bash
python solve_sudoku.py
```

This will:
1. Load all puzzle files (easy.txt, medium.txt, hard.txt, veryhard.txt)
2. Solve each puzzle using the CSP solver
3. Generate a comprehensive report (sudoku_report.txt)
4. Display statistics and analysis

### Validating Puzzles

```bash
python validate_puzzles.py
```

Checks puzzle files for validity (no duplicate values in rows, columns, or boxes).

### Finding Conflicts

```bash
python find_conflicts.py
```

Identifies specific constraint violations in puzzle files.

## Input Format

Puzzle files must contain:
- Exactly 9 lines
- Exactly 9 digits per line (0-9)
- 0 represents an empty cell
- 1-9 represent clues

Example (easy.txt):
```
004030050
609400000
005100489
000060930
300807002
026040000
453009600
000004705
090050200
```

## Results Summary

### All Four Puzzles Solved Successfully ✓

| Puzzle    | Status  | Backtrack Calls | Failures | Time (s) |
|-----------|---------|-----------------|----------|----------|
| Easy      | ✓ SOLVED| 82              | 0        | 0.47     |
| Medium    | ✓ SOLVED| 90              | 8        | 0.39     |
| Hard      | ✓ SOLVED| 139             | 57       | 0.64     |
| Very Hard | ✓ SOLVED| 89              | 7        | 0.41     |
| **TOTAL** | **4/4** | **400**         | **72**   | **1.92** |

### Performance Analysis

#### Easy Puzzle
- **Backtrack Calls**: 82
- **Backtrack Failures**: 0
- **Success Rate**: 100%
- **Analysis**: Minimal backtracking needed due to many clues and simple constraint structure. Forward checking alone nearly solves the puzzle.

#### Medium Puzzle
- **Backtrack Calls**: 90
- **Backtrack Failures**: 8
- **Success Rate**: 91.11%
- **Analysis**: Moderate complexity. Only 8 failures needed despite fewer clues. AC-3 significantly reduces search space.

#### Hard Puzzle
- **Backtrack Calls**: 139
- **Backtrack Failures**: 57
- **Success Rate**: 58.99%
- **Analysis**: Significant backtracking required. 57 failures indicate algorithm explores multiple branches. Still efficient due to constraint propagation.

#### Very Hard Puzzle
- **Backtrack Calls**: 89
- **Backtrack Failures**: 7
- **Success Rate**: 92.13%
- **Analysis**: Despite "very hard" label, requires less backtracking than standard hard puzzles. Good initial constraint propagation reduces branching factor.

### Key Observations

1. **Efficiency of AC-3**: The algorithm reduces domains substantially, leading to fewer backtracks than pure backtracking search.

2. **MRV Heuristic Impact**: Selecting variables with smallest domains first dramatically reduces branching factor.

3. **Forward Checking**: Domain wipe-out detection prevents exploring dead-end branches early.

4. **Puzzle Difficulty Correlation**: Backtrack call count generally correlates with perceived difficulty, but not always linearly. Some "very hard" puzzles may have better constraint structure.

5. **Solution Quality**: All puzzles solved under 1 second, demonstrating effectiveness of combined approach.

## Code Components

### SudokuCSP Class

#### Key Methods:
- `__init__(puzzle)`: Initialize CSP from puzzle string
- `solve()`: Main solving algorithm
- `backtrack(domains)`: Backtracking search with statistics
- `ac3(domains)`: Arc consistency constraint propagation
- `forward_check(var, value, domains)`: Forward checking
- `is_consistent(var, value, assignment)`: Check assignment legality
- `select_unassigned_variable(domains)`: MRV heuristic
- `get_solution()`: Return solution as string
- `get_stats()`: Return backtrack statistics

### SudokuSolverRunner Class

Orchestrates solving multiple puzzles and generating reports with:
- Puzzle loading from files
- Statistics collection
- Report generation with formatted output

## Implementation Highlights

### Constraint Propagation
```python
# AC-3 maintains arc consistency
def ac3(self, domains):
    queue = [(xi, xj) for xi in self.variables for xj in self.constraints[xi]]
    while queue:
        xi, xj = queue.pop(0)
        if self._revise(xi, xj, domains):
            if len(domains[xi]) == 0:
                return False
            for xk in self.constraints[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True
```

### Variable Selection Heuristic
```python
# Minimum Remaining Values (MRV)
def select_unassigned_variable(self, domains):
    unassigned = [var for var in self.variables if var not in self.assignment]
    return min(unassigned, key=lambda var: len(domains[var]))
```

### Backtracking with Pruning
```python
def backtrack(self, domains):
    # Try to assign next variable
    var = self.select_unassigned_variable(domains)
    for value in domains[var]:
        if self.is_consistent(var, value, self.assignment):
            self.assignment[var] = value
            # Forward check + AC-3
            if self.forward_check(var, value, domains) and self.ac3(domains):
                if self.backtrack(domains):
                    return True
            # Backtrack
            del self.assignment[var]
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Running the Solver

```bash
# Solve all puzzles and generate report
python solve_sudoku.py

# Validate puzzle files
python validate_puzzles.py

# Find conflicts in puzzles
python find_conflicts.py
```

## Output

The solver generates:
1. Console output with real-time solving status
2. `sudoku_report.txt` - Comprehensive report including:
   - Original puzzle configuration
   - Complete solution
   - Statistics (backtrack calls, failures, time)
   - Difficulty analysis
   - Summary across all puzzles

## Algorithm Complexity

**Time Complexity**: O(n^m) worst case, where n=9 (domain size) and m=81 (variables), but typically much better due to:
- Constraint propagation reducing effective domain sizes
- MRV heuristic reducing branching factor
- Early detection of inconsistencies

**Space Complexity**: O(m) for storing assignment and domains, O(m²) for constraint graphs

## Future Enhancements

- Parallel solving of independent subproblems
- Advanced heuristics (Least Constraining Value)
- Constraint learning from conflicts
- Support for alternative Sudoku variants
- GUI for interactive solving
- Benchmark against other algorithms

