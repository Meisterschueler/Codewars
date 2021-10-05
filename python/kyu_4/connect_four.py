import numpy as np

def who_is_winner(pieces_position_list):
    field = np.zeros((6,7))
    for piece in pieces_position_list:
        (column,color) = piece.split('_')
        (row,col) = (0, ord(column) - ord('A'))
        
        while field[row,col] != 0:
            row += 1
        field[row,col] = 1 if color == 'Yellow' else 2
    
        for _ in range(4):
            (max_rows, max_cols) = field.shape
            
            # Check horizontal
            for row in range(max_rows):
                for col in range(max_cols-3):
                    if field[row,col] in (1,2):
                        if all(field[row,col] == field[row,col+i] for i in range(1,4)):
                            return "Yellow" if field[row,col] == 1 else "Red"

            # Check diagonal
            for row in range(max_rows-3):
                for col in range(max_cols-3):
                    if field[row,col] in (1,2):
                        if all(field[row,col] == field[row+i,col+i] for i in range(1,4)):
                            return "Yellow" if field[row,col] == 1 else "Red"
            
            field = np.rot90(field)
        
    return "Draw"
