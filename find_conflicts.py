"""
Identify conflicting cells in puzzle transcriptions
"""

def find_conflicts(puzzle_str, name):
    """Find all constraint violations in a puzzle."""
    errors = []
    
    # Check columns
    for col in range(9):
        col_vals = {}
        for row in range(9):
            idx = row * 9 + col
            digit = puzzle_str[idx]
            if digit != '0':
                if digit in col_vals:
                    errors.append(f"Column {col+1}: '{digit}' at rows {col_vals[digit]+1} and {row+1}")
                else:
                    col_vals[digit] = row
    
    # Check rows
    for row in range(9):
        row_vals = {}
        row_str = puzzle_str[row*9:(row+1)*9]
        for col, digit in enumerate(row_str):
            if digit != '0':
                if digit in row_vals:
                    errors.append(f"Row {row+1}: '{digit}' at columns {row_vals[digit]+1} and {col+1}")
                else:
                    row_vals[digit] = col
    
    # Check boxes
    for box_r in range(3):
        for box_c in range(3):
            box_vals = {}
            for r in range(3):
                for c in range(3):
                    idx = (box_r*3+r)*9 + (box_c*3+c)
                    digit = puzzle_str[idx]
                    if digit != '0':
                        if digit in box_vals:
                            errors.append(f"Box ({box_r+1},{box_c+1}): '{digit}' conflict")
                        else:
                            box_vals[digit] = idx
    
    print(f"\n{name}:")
    if errors:
        for error in errors:
            print(f"  ✗ {error}")
    else:
        print(f"  ✓ No conflicts found")


# Test all puzzles
puzzles = {}
for filename, name in [('medium.txt', 'Medium'), ('hard.txt', 'Hard'), ('veryhard.txt', 'Very Hard')]:
    try:
        with open(filename, 'r') as f:
            puzzle = ''.join(f.read().split())
        puzzles[name] = puzzle
    except:
        pass

for name, puzzle in puzzles.items():
    find_conflicts(puzzle, name)
