"""
Validate Sudoku puzzle configurations
"""

def is_valid_puzzle(puzzle_str):
    """Check if puzzle string is a valid Sudoku configuration."""
    if len(puzzle_str) != 81:
        return False, "Invalid length"
    
    if not all(c in '0123456789' for c in puzzle_str):
        return False, "Invalid characters"
    
    # Check for duplicates in rows, columns, and boxes
    for i in range(9):
        # Check row
        row = puzzle_str[i*9:(i+1)*9]
        non_zero = [c for c in row if c != '0']
        if len(non_zero) != len(set(non_zero)):
            return False, f"Row {i+1} has duplicates"
        
        # Check column
        col = ''.join([puzzle_str[j*9+i] for j in range(9)])
        non_zero = [c for c in col if c != '0']
        if len(non_zero) != len(set(non_zero)):
            return False, f"Column {i+1} has duplicates"
    
    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            box = ''
            for r in range(3):
                for c in range(3):
                    idx = (box_row*3+r)*9 + (box_col*3+c)
                    box += puzzle_str[idx]
            non_zero = [c for c in box if c != '0']
            if len(non_zero) != len(set(non_zero)):
                return False, f"Box ({box_row},{box_col}) has duplicates"
    
    return True, "Valid"


# Test all puzzles
puzzles = {}
for filename, name in [('easy.txt', 'Easy'), ('medium.txt', 'Medium'), 
                        ('hard.txt', 'Hard'), ('veryhard.txt', 'Very Hard')]:
    try:
        with open(filename, 'r') as f:
            puzzle = ''.join(f.read().split())
        puzzles[name] = puzzle
    except:
        pass

for name, puzzle in puzzles.items():
    valid, msg = is_valid_puzzle(puzzle)
    print(f"{name:12} | {msg}")
