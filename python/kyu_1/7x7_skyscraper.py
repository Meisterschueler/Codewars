from itertools import permutations
from copy import deepcopy

N = 7

def sight(skyscrapers):
    """Returns how many skyscrapers are in sight from left and from right site."""
    
    max_height_left = 0
    max_height_right = 0
    count_left = 0
    count_right = 0
    
    for i in range(N):
        if skyscrapers[i] > max_height_left:
            max_height_left = skyscrapers[i]
            count_left += 1

        if skyscrapers[N-1-i] > max_height_right:
            max_height_right = skyscrapers[N-1-i]
            count_right += 1
    
    return (count_left, count_right)

def reduce_value_matrix(matrix):
    """Check the value matrix for single possible values and reduce the matrix."""
    
    matrix_prev = None
    while matrix_prev != matrix:
        matrix_prev = matrix
        
        # reduce if only one possible value found: [[1,2], [2,3], [1,2]] => [[1,2], [3], [1,2]]
        for i in range(N):
            for j in range(N):
                if len(matrix[i][j]) > 1:
                    for height in matrix[i][j]:
                        row_singleton = not any([height == e for j2 in list(range(0, j)) + list(range(j+1, N)) for e in matrix[i][j2]])
                        col_singleton = not any([height == e for i2 in list(range(0, i)) + list(range(i+1, N)) for e in matrix[i2][j]])
                        
                        if row_singleton or col_singleton:
                            matrix[i][j] = [height]

        # clear if one possible value available: [[1,2], [1], [1,2,3]] => [[2], [1], [2,3]]
        for i in range(N):
            for j in range(N):
                if len(matrix[i][j]) == 1:
                    for i2 in list(range(0, i)) + list(range(i+1, N)):
                        matrix[i2][j] = [e for e in matrix[i2][j] if e not in matrix[i][j]]
                    for j2 in list(range(0, j)) + list(range(j+1, N)):
                        matrix[i][j2] = [e for e in matrix[i][j2] if e not in matrix[i][j]]
    
    return matrix

def init_poss(clues):
    """Compute all possibilities for each row/column valid for the clues."""
    
    perms = {p: sight(p) for p in permutations([e for e in range(1, N+1)])}
    rows_poss = [None]*N
    for i in range(N):
        rows_poss[i] = [k for k,v in perms.items() if 
                      (clues[4*N-1-i] == v[0] > 0 and clues[N+i] == v[1] > 0)
                      or (clues[4*N-1-i] == v[0] > 0 and clues[N+i] == 0)
                      or (clues[4*N-1-i] == 0 and clues[N+i] == v[1] > 0)
                      or (clues[4*N-1-i] == 0 and clues[N+i] == 0)]
    
    cols_poss = [None]*N
    for i in range(N):
        cols_poss[i] = [k for k,v in perms.items() if 
                      (clues[i] == v[0] > 0 and clues[3*N-1-i] == v[1] > 0)
                      or (clues[i] == v[0] > 0 and clues[3*N-1-i] == 0)
                      or (clues[i] == 0 and clues[3*N-1-i] == v[1] > 0)
                      or (clues[i] == 0 and clues[3*N-1-i] == 0)]
    
    return (rows_poss, cols_poss)
    
def merge_matrices(matrix1, matrix2):
    """Calculate Schnittmenge from two value matrices."""
    
    result = [[None for i in range(N)] for j in range(N)]
    for i in range(N):
        for j in range(N):
            result[i][j] = [x for x in matrix1[i][j] if x in matrix2[i][j]]
    
    return result
    
def calculate_matrices(rows_poss, cols_poss):
    """Calculate value matrices from possibilities."""
    
    rows_matrix = [[None for i in range(N)] for j in range(N)]
    cols_matrix = [[None for i in range(N)] for j in range(N)]
    for i in range(N):
        row_poss = rows_poss[i]
        col_poss = cols_poss[i]
        for j in range(N):
            rows_matrix[i][j] = [altitude for altitude in range(1,N+1) if altitude in [row_po[j] for row_po in row_poss]]
            cols_matrix[j][i] = [altitude for altitude in range(1,N+1) if altitude in [col_po[j] for col_po in col_poss]]

    return rows_matrix, cols_matrix

def print_matrix(clues, matrix):
    for row in range(N+2):
        e = []
        for col in range(N+2):
            if (row,col) == (0,0):
                e.append('\\')
            elif (row,col) == (0,N+1):
                e.append('/')
            elif row == 0:
                e.append(str(clues[col-1]))
            elif (row,col) == (N+1,0):
                e.append('/')
            elif (row,col) == (N+1,N+1):
                e.append('\\')
            elif row == N+1:
                e.append(str(clues[3*N-col]))
            elif col == 0:
                e.append(str(clues[4*N-row]))
            elif col == N+1:
                e.append(str(clues[N+row-1]))
            else:
                e.append('.' if len(matrix[row-1][col-1]) > 1 else str(matrix[row-1][col-1][0]))
        print(" ".join(e))

def print_rows(rows):
    print("\n".join([str(row) for row in rows]))

def solve(rows_poss, cols_poss):
    """Solve field with rows- and cols-possibilities."""
    
    (value_matrix, value_matrix_old, rows_poss_old, cols_poss_old) = (None, None, None, None)
    while value_matrix != value_matrix_old or rows_poss != rows_poss_old or cols_poss != cols_poss_old:
        (value_matrix_old, rows_poss_old, cols_poss_old) = (value_matrix, rows_poss, cols_poss)
        
        rows_matrix, cols_matrix = calculate_matrices(rows_poss, cols_poss)
        value_matrix = merge_matrices(rows_matrix, cols_matrix)
        value_matrix = reduce_value_matrix(value_matrix)
        
        # make rows_poss/cols_poss compatible to the value_matrix
        for i in range(N):
            rows_poss[i] = list(filter(lambda poss: all([e in value_matrix[i][j] for j,e in enumerate(poss)]), rows_poss[i]))
            cols_poss[i] = list(filter(lambda poss: all([e in value_matrix[j][i] for j,e in enumerate(poss)]), cols_poss[i]))
    
    return rows_poss, cols_poss, value_matrix

def is_solved(rows_poss):
    """Check if solved."""

    return all([len(poss) == 1 for poss in rows_poss])

def is_wrong(matrix):
    """If any element is [] then we are on the wrong way."""
    
    return any([len(element) == 0 for row in matrix for element in row])

def solve_puzzle (clues):
    rows_poss, cols_poss = init_poss(clues)
    rows_poss, cols_poss, value_matrix = solve(rows_poss, cols_poss)
    if is_solved(rows_poss):
        return [list(poss[0]) for poss in rows_poss]
    else:
        # try out the possibilities for first row
        for mod in rows_poss[0]:
            rows_poss_mod = deepcopy(rows_poss)
            rows_poss_mod[0] = [mod]
            cols_poss_mod = deepcopy(cols_poss)
            rows_poss_mod, cols_poss_mod, value_matrix = solve(rows_poss_mod, cols_poss_mod)
            if is_solved(rows_poss_mod):
                return [list(poss[0]) for poss in rows_poss_mod]
            elif is_wrong(value_matrix):
                print("NOT SOLVABLE")
            else:
                print("AGAIN A POINT WHERE THE SOLVER FAILS")
            
        print("Here is my state:")
        print_matrix(clues, value_matrix)
