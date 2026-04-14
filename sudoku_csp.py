"""
CSP-Based Sudoku Solver
Uses Backtracking Search with Forward Checking and AC-3 constraint propagation
Author: Sudoku CSP Solver
"""

from typing import Dict, Set, Tuple, List, Optional
from copy import deepcopy

class SudokuCSP:
    """
    Constraint Satisfaction Problem solver for Sudoku puzzles.
    Variables: 81 cells (0-80)
    Domain: Each cell contains digits 1-9
    Constraints: Row, Column, and 3x3 Box constraints
    """
    
    def __init__(self, puzzle: str):
        """
        Initialize the CSP with a Sudoku puzzle.
        
        Args:
            puzzle: String of 81 digits where 0 represents empty cells
        """
        self.puzzle = puzzle
        self.variables = list(range(81))  # Cells 0-80
        self.domains = self._initialize_domains(puzzle)
        self.constraints = self._build_constraints()
        
        # Statistics tracking
        self.backtrack_calls = 0
        self.backtrack_failures = 0
        self.assignment = {}
        
    def _initialize_domains(self, puzzle: str) -> Dict[int, Set[int]]:
        """
        Initialize variable domains based on the puzzle.
        Assigned cells have domain {digit}, unassigned cells have {1-9}.
        
        Args:
            puzzle: Puzzle string
            
        Returns:
            Dictionary mapping variable to its domain (set of possible values)
        """
        domains = {}
        for var in range(81):
            digit = int(puzzle[var])
            if digit != 0:
                # Assigned cell
                domains[var] = {digit}
            else:
                # Unassigned cell - all digits possible
                domains[var] = set(range(1, 10))
        return domains
    
    def _build_constraints(self) -> Dict[int, Set[int]]:
        """
        Build constraint graph mapping each variable to its neighbors.
        Neighbors are variables in the same row, column, or 3x3 box.
        
        Returns:
            Dictionary mapping variable to set of neighboring variables
        """
        constraints = {var: set() for var in range(81)}
        
        for var in range(81):
            row, col = divmod(var, 9)
            
            # Add row neighbors
            for c in range(9):
                neighbor = row * 9 + c
                if neighbor != var:
                    constraints[var].add(neighbor)
            
            # Add column neighbors
            for r in range(9):
                neighbor = r * 9 + col
                if neighbor != var:
                    constraints[var].add(neighbor)
            
            # Add 3x3 box neighbors
            box_row, box_col = (row // 3) * 3, (col // 3) * 3
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    neighbor = r * 9 + c
                    if neighbor != var:
                        constraints[var].add(neighbor)
        
        return constraints
    
    def is_consistent(self, var: int, value: int, 
                     assignment: Dict[int, int]) -> bool:
        """
        Check if assigning value to var is consistent with constraints.
        
        Args:
            var: Variable to assign
            value: Value to assign
            assignment: Current assignment
            
        Returns:
            True if assignment is consistent, False otherwise
        """
        for neighbor in self.constraints[var]:
            if neighbor in assignment:
                if assignment[neighbor] == value:
                    return False
        return True
    
    def ac3(self, domains: Dict[int, Set[int]]) -> bool:
        """
        AC-3 Algorithm: Enforce arc consistency.
        Reduces domains by removing values that have no consistent assignment.
        
        Args:
            domains: Current variable domains
            
        Returns:
            True if consistent, False if inconsistency detected
        """
        # Build queue of all arcs
        queue = []
        for var in self.variables:
            for neighbor in self.constraints[var]:
                queue.append((var, neighbor))
        
        while queue:
            xi, xj = queue.pop(0)
            
            # Revise domain of xi
            if self._revise(xi, xj, domains):
                # Domain of xi was revised
                if len(domains[xi]) == 0:
                    # Inconsistency detected
                    return False
                
                # Add remaining neighbors of xi to queue
                for xk in self.constraints[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        
        return True
    
    def _revise(self, xi: int, xj: int, 
               domains: Dict[int, Set[int]]) -> bool:
        """
        Revise domain of xi with respect to xj.
        Remove values from xi that have no consistent value in xj.
        
        Args:
            xi: Primary variable
            xj: Secondary variable (neighbor)
            domains: Current variable domains
            
        Returns:
            True if domain of xi was revised, False otherwise
        """
        revised = False
        to_remove = set()
        
        for vi in domains[xi]:
            # Check if there's a value in xj's domain consistent with vi
            has_support = False
            for vj in domains[xj]:
                if vi != vj:  # Different values satisfy constraint
                    has_support = True
                    break
            
            if not has_support:
                to_remove.add(vi)
                revised = True
        
        domains[xi] -= to_remove
        return revised
    
    def forward_check(self, var: int, value: int,
                     domains: Dict[int, Set[int]]) -> bool:
        """
        Forward Checking: Remove inconsistent values from neighbor domains.
        
        Args:
            var: Assigned variable
            value: Assigned value
            domains: Current variable domains
            
        Returns:
            True if forward check succeeds, False if domain wipe-out detected
        """
        for neighbor in self.constraints[var]:
            if neighbor not in self.assignment:
                if value in domains[neighbor]:
                    domains[neighbor].remove(value)
                    
                if len(domains[neighbor]) == 0:
                    # Domain wipe-out
                    return False
        
        return True
    
    def select_unassigned_variable(self, domains: Dict[int, Set[int]]) -> Optional[int]:
        """
        Select unassigned variable using Minimum Remaining Values (MRV) heuristic.
        Choose variable with smallest domain size (most constrained).
        
        Args:
            domains: Current variable domains
            
        Returns:
            Selected variable or None if all assigned
        """
        unassigned = [var for var in self.variables if var not in self.assignment]
        
        if not unassigned:
            return None
        
        # MRV heuristic: choose variable with smallest domain
        return min(unassigned, key=lambda var: len(domains[var]))
    
    def backtrack(self, domains: Dict[int, Set[int]]) -> bool:
        """
        Backtracking search with forward checking and AC-3.
        
        Args:
            domains: Current variable domains
            
        Returns:
            True if solution found, False otherwise
        """
        self.backtrack_calls += 1
        
        # Select unassigned variable
        var = self.select_unassigned_variable(domains)
        
        if var is None:
            # All variables assigned - solution found
            return True
        
        # Try each value in domain
        for value in list(domains[var]):  # Copy to avoid modification during iteration
            if self.is_consistent(var, value, self.assignment):
                # Assign variable
                self.assignment[var] = value
                
                # Save domain state for restoration
                saved_domains = deepcopy(domains)
                domains[var] = {value}
                
                # Apply forward checking
                fc_success = self.forward_check(var, value, domains)
                ac3_success = True
                
                # Apply AC-3 if forward checking succeeded
                if fc_success:
                    ac3_success = self.ac3(domains)
                
                # Recursively try to complete assignment
                if fc_success and ac3_success and self.backtrack(domains):
                    return True
                
                # Backtrack: undo assignment and restore domains
                del self.assignment[var]
                domains.clear()
                domains.update(saved_domains)
        
        # No solution found - mark as failure
        self.backtrack_failures += 1
        return False
    
    def solve(self) -> bool:
        """
        Solve the Sudoku puzzle using CSP with backtracking.
        
        Returns:
            True if solved, False if no solution exists
        """
        # Initialize domains from puzzle
        domains = deepcopy(self.domains)
        
        # Apply initial AC-3 to reduce domains
        if not self.ac3(domains):
            return False
        
        # Start backtracking search
        return self.backtrack(domains)
    
    def get_solution(self) -> str:
        """
        Get solution as a string of 81 digits.
        
        Returns:
            Solution string, or empty if not solved
        """
        if len(self.assignment) != 81:
            return ""
        
        solution = ['0'] * 81
        for var, value in self.assignment.items():
            solution[var] = str(value)
        
        return ''.join(solution)
    
    def get_solution_formatted(self) -> str:
        """
        Get solution in formatted 9x9 grid.
        
        Returns:
            Formatted solution string
        """
        solution = self.get_solution()
        if not solution:
            return ""
        
        result = []
        for i in range(9):
            result.append(solution[i*9:(i+1)*9])
        
        return '\n'.join(result)
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get solver statistics.
        
        Returns:
            Dictionary with backtrack_calls and backtrack_failures
        """
        return {
            'backtrack_calls': self.backtrack_calls,
            'backtrack_failures': self.backtrack_failures
        }


def print_sudoku(puzzle_str: str, title: str = "Sudoku"):
    """
    Print a Sudoku puzzle in formatted grid.
    
    Args:
        puzzle_str: Puzzle string of 81 digits
        title: Title for the puzzle
    """
    print(f"\n{title}:")
    print("-" * 25)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 25)
        
        row = puzzle_str[i*9:(i+1)*9]
        row_formatted = []
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row_formatted.append("| ")
            digit = row[j]
            row_formatted.append(digit if digit != '0' else '.')
        
        print(" ".join(row_formatted))


if __name__ == "__main__":
    # Example usage
    easy_puzzle = "004030050609400000005100489000060930300807002026040000453009600000004705090050200"
    
    print("=" * 50)
    print("CSP-Based Sudoku Solver")
    print("=" * 50)
    
    print_sudoku(easy_puzzle, "Easy Puzzle")
    
    solver = SudokuCSP(easy_puzzle)
    if solver.solve():
        print_sudoku(solver.get_solution(), "Solution")
        stats = solver.get_stats()
        print(f"\nStatistics:")
        print(f"  Backtrack calls: {stats['backtrack_calls']}")
        print(f"  Backtrack failures: {stats['backtrack_failures']}")
    else:
        print("No solution found!")
