"""
Main Sudoku Solver Runner
This script solves multiple Sudoku puzzles and generates a comprehensive report
with solutions and statistics (backtrack calls and failures).
"""

import os
from pathlib import Path
from sudoku_csp import SudokuCSP, print_sudoku
import time


class SudokuSolverRunner:
    """Runner for solving multiple Sudoku puzzles and generating reports."""
    
    def __init__(self, puzzles_dir: str = "."):
        """
        Initialize the runner.
        
        Args:
            puzzles_dir: Directory containing puzzle files
        """
        self.puzzles_dir = puzzles_dir
        self.results = []
    
    def load_puzzle(self, filename: str) -> str:
        """
        Load puzzle from file.
        
        Args:
            filename: Path to puzzle file
            
        Returns:
            Puzzle string of 81 digits
        """
        with open(filename, 'r') as f:
            # Remove whitespace and newlines
            puzzle = ''.join(f.read().split())
        
        # Validate
        if len(puzzle) != 81:
            raise ValueError(f"Invalid puzzle: expected 81 digits, got {len(puzzle)}")
        
        if not all(c in '0123456789' for c in puzzle):
            raise ValueError("Invalid puzzle: contains non-digit characters")
        
        return puzzle
    
    def solve_puzzle(self, puzzle_str: str, puzzle_name: str) -> dict:
        """
        Solve a single puzzle and record statistics.
        
        Args:
            puzzle_str: Puzzle string
            puzzle_name: Name/identifier for the puzzle
            
        Returns:
            Dictionary with puzzle name, solution, and statistics
        """
        print(f"\nSolving {puzzle_name}...")
        print("-" * 60)
        
        # Time the solver
        start_time = time.time()
        solver = SudokuCSP(puzzle_str)
        solved = solver.solve()
        elapsed_time = time.time() - start_time
        
        stats = solver.get_stats()
        solution = solver.get_solution() if solved else ""
        
        result = {
            'name': puzzle_name,
            'original': puzzle_str,
            'solved': solved,
            'solution': solution,
            'backtrack_calls': stats['backtrack_calls'],
            'backtrack_failures': stats['backtrack_failures'],
            'time': elapsed_time
        }
        
        self.results.append(result)
        
        # Print results
        if solved:
            print(f"✓ Puzzle solved in {elapsed_time:.4f} seconds")
            print(f"  Backtrack calls: {stats['backtrack_calls']}")
            print(f"  Backtrack failures: {stats['backtrack_failures']}")
        else:
            print(f"✗ Puzzle could not be solved")
        
        return result
    
    def run_all_puzzles(self):
        """Solve all puzzle files in the puzzles directory."""
        puzzle_files = [
            ('easy.txt', 'Easy'),
            ('medium.txt', 'Medium'),
            ('hard.txt', 'Hard'),
            ('veryhard.txt', 'Very Hard')
        ]
        
        print("\n" + "=" * 60)
        print("CSP-BASED SUDOKU SOLVER")
        print("with Backtracking, Forward Checking, and AC-3")
        print("=" * 60)
        
        for filename, difficulty in puzzle_files:
            filepath = os.path.join(self.puzzles_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"\n⚠ File not found: {filepath}")
                continue
            
            try:
                puzzle = self.load_puzzle(filepath)
                self.solve_puzzle(puzzle, f"{difficulty} Puzzle")
            except Exception as e:
                print(f"\n✗ Error processing {filename}: {e}")
    
    def generate_report(self, output_file: str = "sudoku_report.txt"):
        """
        Generate a comprehensive report of all solved puzzles.
        
        Args:
            output_file: Path to output report file
        """
        report_lines = [
            "=" * 80,
            "SUDOKU CSP SOLVER - COMPREHENSIVE REPORT",
            "=" * 80,
            "",
            "Algorithm: Backtracking Search with Forward Checking and AC-3",
            "Variable Selection Heuristic: Minimum Remaining Values (MRV)",
            "",
            "=" * 80,
            ""
        ]
        
        for result in self.results:
            report_lines.append(f"\n{result['name'].upper()}")
            report_lines.append("-" * 80)
            report_lines.append("")
            
            # Original puzzle
            report_lines.append("ORIGINAL PUZZLE:")
            puzzle_str = result['original']
            for i in range(9):
                row = puzzle_str[i*9:(i+1)*9]
                row_display = []
                for j in range(9):
                    if j % 3 == 0 and j != 0:
                        row_display.append("| ")
                    digit = row[j]
                    row_display.append(digit if digit != '0' else '.')
                report_lines.append(" ".join(row_display))
                
                if (i + 1) % 3 == 0 and i < 8:
                    report_lines.append("-" * 35)
            
            report_lines.append("")
            
            # Solution
            if result['solved']:
                report_lines.append("SOLUTION:")
                solution_str = result['solution']
                for i in range(9):
                    row = solution_str[i*9:(i+1)*9]
                    row_display = []
                    for j in range(9):
                        if j % 3 == 0 and j != 0:
                            row_display.append("| ")
                        row_display.append(row[j])
                    report_lines.append(" ".join(row_display))
                    
                    if (i + 1) % 3 == 0 and i < 8:
                        report_lines.append("-" * 35)
            else:
                report_lines.append("SOLUTION: No solution found")
            
            report_lines.append("")
            
            # Statistics
            report_lines.append("STATISTICS:")
            report_lines.append(f"  Backtrack function calls:      {result['backtrack_calls']}")
            report_lines.append(f"  Backtrack function failures:   {result['backtrack_failures']}")
            report_lines.append(f"  Time elapsed:                  {result['time']:.4f} seconds")
            report_lines.append("")
            
            # Analysis
            report_lines.append("ANALYSIS:")
            if result['solved']:
                total_calls = result['backtrack_calls']
                failures = result['backtrack_failures']
                success_rate = 100.0 * (total_calls - failures) / total_calls if total_calls > 0 else 0
                
                report_lines.append(f"  Total assignments attempted:  {total_calls}")
                report_lines.append(f"  Failed assignments (backups): {failures}")
                report_lines.append(f"  Success rate:                 {success_rate:.2f}%")
                
                if result['backtrack_calls'] <= 50:
                    report_lines.append("  Difficulty: EASY (minimal backtracking needed)")
                elif result['backtrack_calls'] <= 500:
                    report_lines.append("  Difficulty: MEDIUM (moderate backtracking)")
                elif result['backtrack_calls'] <= 2000:
                    report_lines.append("  Difficulty: HARD (significant backtracking)")
                else:
                    report_lines.append("  Difficulty: EXPERT (extensive backtracking)")
            
            report_lines.append("")
            report_lines.append("=" * 80)
        
        # Summary
        report_lines.append("\nSUMMARY")
        report_lines.append("=" * 80)
        total_solved = sum(1 for r in self.results if r['solved'])
        report_lines.append(f"Total puzzles solved: {total_solved}/{len(self.results)}")
        report_lines.append(f"Total backtrack calls: {sum(r['backtrack_calls'] for r in self.results)}")
        report_lines.append(f"Total backtrack failures: {sum(r['backtrack_failures'] for r in self.results)}")
        report_lines.append(f"Total time: {sum(r['time'] for r in self.results):.4f} seconds")
        
        # Write report
        with open(output_file, 'w') as f:
            f.write('\n'.join(report_lines))
        
        print(f"\n✓ Report generated: {output_file}")
        
        # Also print summary to console
        print("\n" + '\n'.join(report_lines[-10:]))


def main():
    """Main entry point."""
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create and run solver
    runner = SudokuSolverRunner(current_dir)
    runner.run_all_puzzles()
    
    # Generate report
    report_path = os.path.join(current_dir, "sudoku_report.txt")
    runner.generate_report(report_path)
    
    print("\n" + "=" * 80)
    print("SOLVER COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
