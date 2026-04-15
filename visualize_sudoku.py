"""
Sudoku Grid Visualizer
Provides visual representations of Sudoku puzzles and solutions with statistics.
"""

from sudoku_csp import SudokuCSP
import os
import time


class SudokuVisualizer:
    """Visualizer for Sudoku puzzles with grids and statistics."""
    
    @staticmethod
    def format_grid(puzzle_str: str) -> str:
        """
        Format a puzzle string into a visual grid with borders.
        
        Args:
            puzzle_str: String of 81 digits
            
        Returns:
            Formatted grid as a string
        """
        lines = []
        lines.append("╔═══════════════════════════╗")
        
        for row in range(9):
            if row % 3 == 0 and row != 0:
                lines.append("╠═══════╬═══════╬═══════╣")
            
            row_str = ""
            for col in range(9):
                if col % 3 == 0:
                    row_str += "║ "
                
                digit = puzzle_str[row * 9 + col]
                row_str += digit if digit != '0' else '.'
                row_str += " "
            
            row_str += "║"
            lines.append(row_str)
        
        lines.append("╚═══════════════════════════╝")
        return "\n".join(lines)
    
    @staticmethod
    def display_puzzle_and_solution(name: str, original: str, solution: str, stats: dict):
        """
        Display puzzle, solution, and statistics side by side.
        
        Args:
            name: Puzzle name/difficulty
            original: Original puzzle string
            solution: Solved puzzle string
            stats: Statistics dictionary with backtrack_calls, backtrack_failures, time
        """
        print("\n" + "=" * 70)
        print(f"  {name.upper()}")
        print("=" * 70)
        
        # Display grids side by side
        original_lines = SudokuVisualizer.format_grid(original).split('\n')
        solution_lines = SudokuVisualizer.format_grid(solution).split('\n')
        
        print("\n  ORIGINAL PUZZLE              SOLUTION")
        print("  " + "-" * 32 + "  " + "-" * 32)
        
        for orig_line, sol_line in zip(original_lines, solution_lines):
            print(f"  {orig_line}  {sol_line}")
        
        # Display statistics
        print("\n  STATISTICS:")
        print(f"  ├─ Backtrack Calls:      {stats['backtrack_calls']:>8,}")
        print(f"  ├─ Backtrack Failures:   {stats['backtrack_failures']:>8,}")
        print(f"  ├─ Success Rate:         {stats['success_rate']:>7.2f}%")
        print(f"  ├─ Solve Time:           {stats['time']:>8.4f}s")
        
        difficulty = SudokuVisualizer.get_difficulty(stats['backtrack_calls'])
        print(f"  └─ Difficulty:           {difficulty:>15}")
        
        print("\n" + "=" * 70)
    
    @staticmethod
    def get_difficulty(backtrack_calls: int) -> str:
        """
        Determine difficulty level based on backtrack calls.
        
        Args:
            backtrack_calls: Number of backtrack function calls
            
        Returns:
            Difficulty string
        """
        if backtrack_calls <= 50:
            return "EASY"
        elif backtrack_calls <= 500:
            return "MEDIUM"
        elif backtrack_calls <= 2000:
            return "HARD"
        else:
            return "EXPERT"
    
    @staticmethod
    def display_summary(results: list):
        """
        Display summary statistics for all puzzles.
        
        Args:
            results: List of result dictionaries
        """
        print("\n\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 20 + "SUMMARY STATISTICS" + " " * 30 + "║")
        print("╠" + "═" * 68 + "╣")
        
        total_calls = sum(r['backtrack_calls'] for r in results)
        total_failures = sum(r['backtrack_failures'] for r in results)
        total_time = sum(r['time'] for r in results)
        solved = sum(1 for r in results if r['solved'])
        
        print(f"║ Total Puzzles Solved:         {solved}/{len(results):<40}║")
        print(f"║ Total Backtrack Calls:        {total_calls:>12,}{'':<30}║")
        print(f"║ Total Backtrack Failures:     {total_failures:>12,}{'':<30}║")
        print(f"║ Combined Success Rate:        {(100.0 * (total_calls - total_failures) / total_calls if total_calls > 0 else 0):>7.2f}%{'':<29}║")
        print(f"║ Total Solving Time:           {total_time:>12.4f}s{'':<30}║")
        
        print("╚" + "═" * 68 + "╝")
    
    @staticmethod
    def display_puzzle_table(results: list):
        """
        Display a table of all puzzle results.
        
        Args:
            results: List of result dictionaries
        """
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 18 + "PUZZLE RESULTS COMPARISON TABLE" + " " * 20 + "║")
        print("╠" + "═" * 68 + "╣")
        print("║ Puzzle       │ Calls        │ Failures     │ Success    │ Time      ║")
        print("╠" + "═" * 68 + "╣")
        
        for result in results:
            name = result['name'].ljust(12)
            calls = str(result['backtrack_calls']).rjust(12)
            failures = str(result['backtrack_failures']).rjust(12)
            
            total_calls = result['backtrack_calls']
            success_rate = (100.0 * (total_calls - result['backtrack_failures']) / total_calls 
                          if total_calls > 0 else 0)
            success = f"{success_rate:>6.2f}%".rjust(10)
            
            time_str = f"{result['time']:.4f}s".rjust(9)
            
            print(f"║ {name} │ {calls} │ {failures} │ {success} │ {time_str} ║")
        
        print("╚" + "═" * 68 + "╝")


class EnhancedSudokuSolverRunner:
    """Enhanced runner with visual output."""
    
    def __init__(self, puzzles_dir: str = "."):
        """Initialize the runner."""
        self.puzzles_dir = puzzles_dir
        self.results = []
    
    def load_puzzle(self, filename: str) -> str:
        """Load puzzle from file."""
        with open(filename, 'r') as f:
            puzzle = ''.join(f.read().split())
        
        if len(puzzle) != 81:
            raise ValueError(f"Invalid puzzle: expected 81 digits, got {len(puzzle)}")
        
        if not all(c in '0123456789' for c in puzzle):
            raise ValueError("Invalid puzzle: contains non-digit characters")
        
        return puzzle
    
    def solve_puzzle(self, puzzle_str: str, puzzle_name: str) -> dict:
        """Solve a single puzzle and record statistics."""
        print(f"\nSolving {puzzle_name}...")
        
        start_time = time.time()
        solver = SudokuCSP(puzzle_str)
        solved = solver.solve()
        elapsed_time = time.time() - start_time
        
        stats = solver.get_stats()
        solution = solver.get_solution() if solved else ""
        
        total_calls = stats['backtrack_calls']
        failures = stats['backtrack_failures']
        success_rate = 100.0 * (total_calls - failures) / total_calls if total_calls > 0 else 0
        
        result = {
            'name': puzzle_name,
            'original': puzzle_str,
            'solved': solved,
            'solution': solution,
            'backtrack_calls': stats['backtrack_calls'],
            'backtrack_failures': stats['backtrack_failures'],
            'success_rate': success_rate,
            'time': elapsed_time
        }
        
        self.results.append(result)
        
        if solved:
            print(f"✓ Solved in {elapsed_time:.4f}s")
        else:
            print(f"✗ Could not be solved")
        
        return result
    
    def run_all_puzzles(self):
        """Solve all puzzle files."""
        puzzle_files = [
            ('easy.txt', 'Easy'),
            ('medium.txt', 'Medium'),
            ('hard.txt', 'Hard'),
            ('veryhard.txt', 'Very Hard'),
            ('expert.txt', 'Expert')
        ]
        
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 12 + "CSP-BASED SUDOKU SOLVER WITH VISUALIZATION" + " " * 14 + "║")
        print("║" + " " * 8 + "Backtracking, Forward Checking, and AC-3 Constraint Propagation" + " " * -6 + "║")
        print("╚" + "═" * 68 + "╝")
        
        for filename, difficulty in puzzle_files:
            filepath = os.path.join(self.puzzles_dir, filename)
            
            if not os.path.exists(filepath):
                continue
            
            try:
                puzzle = self.load_puzzle(filepath)
                self.solve_puzzle(puzzle, f"{difficulty} Puzzle")
            except Exception as e:
                print(f"\n✗ Error processing {filename}: {e}")
    
    def display_results(self):
        """Display all results with visual components."""
        print("\n\n")
        print("█" * 70)
        print("█" + " " * 68 + "█")
        print("█" + "DETAILED PUZZLE ANALYSIS".center(68) + "█")
        print("█" + " " * 68 + "█")
        print("█" * 70)
        
        for result in self.results:
            if result['solved']:
                SudokuVisualizer.display_puzzle_and_solution(
                    result['name'],
                    result['original'],
                    result['solution'],
                    {
                        'backtrack_calls': result['backtrack_calls'],
                        'backtrack_failures': result['backtrack_failures'],
                        'success_rate': result['success_rate'],
                        'time': result['time']
                    }
                )
        
        # Display comparison table
        SudokuVisualizer.display_puzzle_table(self.results)
        
        # Display summary
        SudokuVisualizer.display_summary(self.results)


def main():
    """Main entry point."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    runner = EnhancedSudokuSolverRunner(current_dir)
    runner.run_all_puzzles()
    runner.display_results()
    
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "VISUALIZATION COMPLETE".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70 + "\n")


if __name__ == "__main__":
    main()
