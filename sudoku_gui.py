"""
Sudoku Solver GUI using Tkinter
Interactive visual interface for solving and displaying Sudoku puzzles.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from sudoku_csp import SudokuCSP
import time


class SudokuGUI:
    """Tkinter GUI for Sudoku solver with visual grid display."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Sudoku CSP Solver - Visual Interface")
        self.root.geometry("1400x800")
        self.root.configure(bg="#2c3e50")
        
        self.puzzles_dir = os.path.dirname(os.path.abspath(__file__))
        self.puzzle_files = [
            ('easy.txt', 'Easy'),
            ('medium.txt', 'Medium'),
            ('hard.txt', 'Hard'),
            ('veryhard.txt', 'Very Hard')
        ]
        
        self.current_puzzle_idx = 0
        self.current_result = None
        self.results = []
        
        self.colors = {
            'bg': '#2c3e50',
            'fg': '#ecf0f1',
            'accent': '#3498db',
            'success': '#2ecc71',
            'error': '#e74c3c',
            'panel': '#34495e'
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        control_frame = tk.Frame(main_frame, bg=self.colors['panel'], relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(control_frame, text="Sudoku CSP Solver", font=("Arial", 18, "bold"), 
                bg=self.colors['panel'], fg=self.colors['accent']).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Puzzle selector
        tk.Label(control_frame, text="Puzzle:", font=("Arial", 10), 
                bg=self.colors['panel'], fg=self.colors['fg']).pack(side=tk.LEFT, padx=10)
        
        self.puzzle_var = tk.StringVar(value="Easy")
        puzzle_menu = ttk.Combobox(control_frame, textvariable=self.puzzle_var, 
                                   values=[name for _, name in self.puzzle_files],
                                   state="readonly", width=12)
        puzzle_menu.pack(side=tk.LEFT, padx=5)
        puzzle_menu.bind("<<ComboboxSelected>>", self.on_puzzle_selected)
        
        # Buttons
        ttk.Button(control_frame, text="Load & Solve", command=self.solve_current).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Solve All", command=self.solve_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.clear_display).pack(side=tk.LEFT, padx=5)
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Grids
        grid_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Original puzzle
        tk.Label(grid_frame, text="ORIGINAL PUZZLE", font=("Arial", 12, "bold"),
                bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=(0, 5))
        
        self.original_canvas = tk.Canvas(grid_frame, width=350, height=350, 
                                        bg="white", relief=tk.SUNKEN, bd=2)
        self.original_canvas.pack(padx=5, pady=(0, 15))
        
        # Solution
        tk.Label(grid_frame, text="SOLUTION", font=("Arial", 12, "bold"),
                bg=self.colors['bg'], fg=self.colors['accent']).pack(pady=(0, 5))
        
        self.solution_canvas = tk.Canvas(grid_frame, width=350, height=350,
                                        bg="white", relief=tk.SUNKEN, bd=2)
        self.solution_canvas.pack(padx=5)
        
        # Right side - Statistics
        stats_frame = tk.Frame(content_frame, bg=self.colors['panel'], relief=tk.RAISED, bd=2)
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        tk.Label(stats_frame, text="STATISTICS", font=("Arial", 14, "bold"),
                bg=self.colors['panel'], fg=self.colors['accent']).pack(pady=10)
        
        # Stats labels
        self.stats_labels = {}
        stats_items = [
            ('puzzle_name', 'Puzzle:'),
            ('status', 'Status:'),
            ('backtrack_calls', 'Backtrack Calls:'),
            ('backtrack_failures', 'Backtrack Failures:'),
            ('success_rate', 'Success Rate:'),
            ('solve_time', 'Solve Time:'),
            ('difficulty', 'Difficulty:')
        ]
        
        for key, label in stats_items:
            frame = tk.Frame(stats_frame, bg=self.colors['panel'])
            frame.pack(fill=tk.X, padx=15, pady=8)
            
            tk.Label(frame, text=label, font=("Arial", 10, "bold"), width=20, anchor="w",
                    bg=self.colors['panel'], fg=self.colors['fg']).pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text="—", font=("Arial", 10),
                                  bg=self.colors['panel'], fg=self.colors['success'])
            value_label.pack(side=tk.LEFT, padx=(10, 0))
            self.stats_labels[key] = value_label
        
        # Summary section
        tk.Label(stats_frame, text="SUMMARY", font=("Arial", 12, "bold"),
                bg=self.colors['panel'], fg=self.colors['accent']).pack(pady=(20, 10))
        
        self.summary_labels = {}
        summary_items = [
            ('total_solved', 'Total Solved:'),
            ('total_calls', 'Total Calls:'),
            ('total_failures', 'Total Failures:'),
            ('total_time', 'Total Time:')
        ]
        
        for key, label in summary_items:
            frame = tk.Frame(stats_frame, bg=self.colors['panel'])
            frame.pack(fill=tk.X, padx=15, pady=6)
            
            tk.Label(frame, text=label, font=("Arial", 9), width=20, anchor="w",
                    bg=self.colors['panel'], fg=self.colors['fg']).pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text="—", font=("Arial", 9),
                                  bg=self.colors['panel'], fg=self.colors['success'])
            value_label.pack(side=tk.LEFT, padx=(10, 0))
            self.summary_labels[key] = value_label
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                             bg=self.colors['accent'], fg=self.colors['bg'],
                             font=("Arial", 10), relief=tk.SUNKEN, bd=1)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def load_puzzle(self, filepath):
        """Load a puzzle from file."""
        with open(filepath, 'r') as f:
            puzzle = ''.join(f.read().split())
        
        if len(puzzle) != 81 or not all(c in '0123456789' for c in puzzle):
            raise ValueError("Invalid puzzle format")
        
        return puzzle
    
    def draw_grid(self, canvas, puzzle_str, title=""):
        """Draw Sudoku grid on canvas."""
        canvas.delete("all")
        
        if not puzzle_str:
            canvas.create_text(175, 175, text="No puzzle loaded", font=("Arial", 12), fill="gray")
            return
        
        cell_size = 35
        border_width = 2
        
        # Draw grid
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            # Vertical lines
            canvas.create_line(i * cell_size, 0, i * cell_size, 350, width=width)
            # Horizontal lines
            canvas.create_line(0, i * cell_size, 350, i * cell_size, width=width)
        
        # Draw numbers
        for idx, digit in enumerate(puzzle_str):
            if digit != '0':
                row = idx // 9
                col = idx % 9
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2
                canvas.create_text(x, y, text=digit, font=("Arial", 16, "bold"), fill="#2c3e50")
    
    def on_puzzle_selected(self, event=None):
        """Handle puzzle selection from dropdown."""
        selected = self.puzzle_var.get()
        self.current_puzzle_idx = next(i for i, (_, name) in enumerate(self.puzzle_files) if name == selected)
        self.clear_display()
    
    def solve_current(self):
        """Solve the currently selected puzzle."""
        puzzle_name = self.puzzle_var.get()
        filename, _ = self.puzzle_files[self.current_puzzle_idx]
        filepath = os.path.join(self.puzzles_dir, filename)
        
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"Puzzle file not found: {filepath}")
            return
        
        try:
            self.status_var.set(f"Solving {puzzle_name}...")
            self.root.update()
            
            puzzle = self.load_puzzle(filepath)
            
            start_time = time.time()
            solver = SudokuCSP(puzzle)
            solved = solver.solve()
            elapsed_time = time.time() - start_time
            
            stats = solver.get_stats()
            solution = solver.get_solution() if solved else ""
            
            total_calls = stats['backtrack_calls']
            failures = stats['backtrack_failures']
            success_rate = 100.0 * (total_calls - failures) / total_calls if total_calls > 0 else 0
            difficulty = self.get_difficulty(total_calls)
            
            self.current_result = {
                'name': puzzle_name,
                'original': puzzle,
                'solved': solved,
                'solution': solution,
                'backtrack_calls': stats['backtrack_calls'],
                'backtrack_failures': failures,
                'success_rate': success_rate,
                'time': elapsed_time,
                'difficulty': difficulty
            }
            
            # Store in results
            self.results.append(self.current_result)
            
            # Display
            self.display_result()
            self.update_summary()
            
            status_msg = f"✓ {puzzle_name} solved in {elapsed_time:.4f}s" if solved else f"✗ {puzzle_name} could not be solved"
            self.status_var.set(status_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to solve puzzle: {str(e)}")
            self.status_var.set("Error occurred")
    
    def solve_all(self):
        """Solve all puzzles."""
        self.results = []
        
        for idx, (filename, name) in enumerate(self.puzzle_files):
            filepath = os.path.join(self.puzzles_dir, filename)
            
            if not os.path.exists(filepath):
                continue
            
            self.puzzle_var.set(name)
            self.root.update()
            
            try:
                puzzle = self.load_puzzle(filepath)
                
                start_time = time.time()
                solver = SudokuCSP(puzzle)
                solved = solver.solve()
                elapsed_time = time.time() - start_time
                
                stats = solver.get_stats()
                solution = solver.get_solution() if solved else ""
                
                total_calls = stats['backtrack_calls']
                failures = stats['backtrack_failures']
                success_rate = 100.0 * (total_calls - failures) / total_calls if total_calls > 0 else 0
                difficulty = self.get_difficulty(total_calls)
                
                self.current_result = {
                    'name': name,
                    'original': puzzle,
                    'solved': solved,
                    'solution': solution,
                    'backtrack_calls': stats['backtrack_calls'],
                    'backtrack_failures': failures,
                    'success_rate': success_rate,
                    'time': elapsed_time,
                    'difficulty': difficulty
                }
                
                self.results.append(self.current_result)
                self.display_result()
                self.update_summary()
                
                self.status_var.set(f"Solved {len(self.results)}/{len(self.puzzle_files)} puzzles...")
                self.root.update()
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error solving {name}: {str(e)}")
        
        self.status_var.set(f"✓ Completed! Solved {len(self.results)}/{len(self.puzzle_files)} puzzles")
    
    def display_result(self):
        """Display current result on grids."""
        if not self.current_result:
            return
        
        self.draw_grid(self.original_canvas, self.current_result['original'])
        self.draw_grid(self.solution_canvas, self.current_result['solution'] if self.current_result['solved'] else "")
        
        # Update stats
        self.stats_labels['puzzle_name'].config(text=self.current_result['name'])
        self.stats_labels['status'].config(
            text="✓ Solved" if self.current_result['solved'] else "✗ Unsolved",
            fg=self.colors['success'] if self.current_result['solved'] else self.colors['error']
        )
        self.stats_labels['backtrack_calls'].config(text=f"{self.current_result['backtrack_calls']:,}")
        self.stats_labels['backtrack_failures'].config(text=f"{self.current_result['backtrack_failures']:,}")
        self.stats_labels['success_rate'].config(text=f"{self.current_result['success_rate']:.2f}%")
        self.stats_labels['solve_time'].config(text=f"{self.current_result['time']:.4f}s")
        self.stats_labels['difficulty'].config(text=self.current_result['difficulty'])
    
    def update_summary(self):
        """Update summary statistics."""
        if not self.results:
            return
        
        total_solved = sum(1 for r in self.results if r['solved'])
        total_calls = sum(r['backtrack_calls'] for r in self.results)
        total_failures = sum(r['backtrack_failures'] for r in self.results)
        total_time = sum(r['time'] for r in self.results)
        
        self.summary_labels['total_solved'].config(text=f"{total_solved}/{len(self.results)}")
        self.summary_labels['total_calls'].config(text=f"{total_calls:,}")
        self.summary_labels['total_failures'].config(text=f"{total_failures:,}")
        self.summary_labels['total_time'].config(text=f"{total_time:.4f}s")
    
    def clear_display(self):
        """Clear display."""
        self.current_result = None
        self.original_canvas.delete("all")
        self.solution_canvas.delete("all")
        
        for label in self.stats_labels.values():
            label.config(text="—")
        
        self.status_var.set("Ready")
    
    def get_difficulty(self, backtrack_calls):
        """Get difficulty string based on backtrack calls."""
        if backtrack_calls <= 50:
            return "EASY"
        elif backtrack_calls <= 500:
            return "MEDIUM"
        elif backtrack_calls <= 2000:
            return "HARD"
        else:
            return "EXPERT"


def main():
    """Main entry point."""
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
