import numpy as np

def possible_numbers(puzzle, i, j):
    return list(sorted([x for x in range(1,10) if x not in puzzle[i,:] and x not in puzzle[:,j] and not np.any(puzzle[i-(i%3):i-(i%3)+3, j-(j%3):j-(j%3)+3] == x)]))

def get_probability_matrix(puzzle):
    result = np.zeros((9,9), dtype=object)
    for i in range(9):
        for j in range(9):
            if puzzle[i,j] == 0:
                result[i,j] = possible_numbers(puzzle, i, j)
            else:
                result[i,j] = puzzle[i,j]
    return result

def sudoku(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
    P = get_probability_matrix(np.matrix(puzzle))

    changed = True
    while changed:
        changed = False
        for i in range(9):
            for j in range(9):
                if isinstance(P[i,j], list):
                    p1 = P[i,j]
                    if len(p1) == 1:    # single found
                        p1 = p1[0]
                        for ii in range(9):
                            if ii != i and isinstance(P[ii,j], list) and p1 in P[ii,j]:    # remove from same column
                                P[ii,j].remove(p1)
                        for jj in range(9):
                            if jj != j and isinstance(P[i,jj], list) and p1 in P[i,jj]:    # remove from same row
                                P[i,jj].remove(p1)
                        for ii in range(i-(i%3), i-(i%3)+3):
                            for jj in range(j-(j%3), j-(j%3)+3):
                                if not (ii == i and jj == j) and isinstance(P[ii,jj], list) and p1 in P[ii,jj]:    # remove from submatrix
                                    P[ii,jj].remove(p1)
                        P[i,j] = p1
                        changed = True
                    elif len(p1) == 2:    # pair found
                        for ii in range(9):
                            if ii != i and isinstance(P[ii,j], list) and p1 == P[ii,j]:    # twins same column found
                                for twin_number in p1:
                                    for iii in range(9):
                                        if iii not in (i, ii) and isinstance(P[iii,j], list) and twin_number in P[iii,j]:
                                            P[iii,j].remove(twin_number)
                                            changed = True
                            
                        for jj in range(9):
                            if jj != j and isinstance(P[i,jj], list) and p1 == P[i,jj]:    # twins in same row found
                                for twin_number in p1:
                                    for jjj in range(9):
                                        if jjj not in (j, jj) and isinstance(P[i,jjj], list) and twin_number in P[i,jjj]:
                                            P[i,jjj].remove(twin_number)
                                            changed = True 
    return P.tolist()
