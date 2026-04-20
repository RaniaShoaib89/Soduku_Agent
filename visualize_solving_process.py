"""
Interactive Sudoku Solving Process Visualizer
Displays the step-by-step solving process as a human would solve it.
"""

from sudoku_csp import SudokuCSP
from visualize_sudoku import SudokuVisualizer
import os
import sys


def load_puzzle(filename: str) -> str:
    """Load puzzle from file."""
    try:
        with open(filename, 'r') as f:
            puzzle = ''.join(f.read().split())
        
        if len(puzzle) != 81:
            raise ValueError(f"Invalid puzzle: expected 81 digits, got {len(puzzle)}")
        
        if not all(c in '0123456789' for c in puzzle):
            raise ValueError("Invalid puzzle: contains non-digit characters")
        
        return puzzle
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        return None


def interactive_solve_with_visualization():
    """
    Interactively select a puzzle and visualize its solving process.
    """
    print("\n" + "=" * 70)
    print("  SUDOKU SOLVER - STEP-BY-STEP VISUALIZATION")
    print("=" * 70)
    
    puzzle_files = [
        ('easy.txt', 'Easy'),
        ('medium.txt', 'Medium'),
        ('hard.txt', 'Hard'),
        ('veryhard.txt', 'Very Hard'),
    ]
    
    print("\nAvailable puzzles:")
    valid_files = []
    for i, (filename, difficulty) in enumerate(puzzle_files, 1):
        if os.path.exists(filename):
            print(f"  {i}. {difficulty} ({filename})")
            valid_files.append((filename, difficulty))
    
    if not valid_files:
        print("\n❌ No puzzle files found!")
        return
    
    # Get user selection
    while True:
        try:
            choice = input("\nSelect a puzzle (enter number): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(valid_files):
                filename, difficulty = valid_files[idx]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Load and solve puzzle
    print(f"\n📂 Loading {difficulty} puzzle...")
    puzzle = load_puzzle(filename)
    if puzzle is None:
        return
    
    # Show original puzzle
    print(f"\n🧩 Original Puzzle:")
    print(SudokuVisualizer.format_grid(puzzle))
    empty_cells = sum(1 for c in puzzle if c == '0')
    print(f"   Empty cells: {empty_cells}/81")
    
    # Solve with visualization
    print(f"\n⚙️  Solving puzzle using CSP with Backtracking, Forward Checking, and AC-3...")
    solver = SudokuCSP(puzzle)
    solved = solver.solve()
    
    if not solved:
        print("❌ Could not solve this puzzle!")
        return
    
    stats = solver.get_stats()
    print(f"\n✅ Puzzle solved!")
    print(f"   Backtrack calls: {stats['backtrack_calls']:,}")
    print(f"   Backtrack failures: {stats['backtrack_failures']:,}")
    
    # Ask for animation speed
    print("\n🎬 Visualization Options:")
    print("  1. Fast (0.02s per step) - Best for hard puzzles")
    print("  2. Normal (0.05s per step) - Default speed")
    print("  3. Slow (0.1s per step) - Best for learning")
    print("  4. Very Slow (0.2s per step) - Detailed observation")
    
    speed_choice = input("\nSelect speed (1-4, default 2): ").strip()
    delays = {'1': 0.02, '2': 0.05, '3': 0.1, '4': 0.2}
    delay = delays.get(speed_choice, 0.05)
    
    # Show animation
    print("\n" + "=" * 70)
    input("Press Enter to start the animation...")
    SudokuVisualizer.display_solving_animation(puzzle, solver, delay=delay)
    
    # Show summary
    print("\n📊 SUMMARY:")
    print(f"   Total steps: {len(solver.get_steps())}")
    print(f"   Solve time: {solver.get_stats()['backtrack_calls']} backtrack calls")
    
    print("\n✨ Visualization complete!")


if __name__ == "__main__":
    try:
        interactive_solve_with_visualization()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
