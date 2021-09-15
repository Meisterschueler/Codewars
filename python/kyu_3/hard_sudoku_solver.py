from copy import deepcopy

def sudoku_print(P):
    for row in range(9):
        for col in range(9):
            cell = P[row][col]
            string = ''.join([str(c) for c in cell])
            print(f"{string:10s}" if col in (2,5) else f"{string:5s}", end='')
        print()
        if row in (2,5):
            print()
    print("--------------------------------------------------------------------------")

def naked_single(P, pi, pj):
    value = P[pi][pj][0]
    for i in range(9):
        if i != pi and value in P[i][pj]:
            P[i][pj].remove(value)
            listlen = len(P[i][pj])
            if listlen == 0:
                return None
            elif listlen == 1:
                P = naked_single(P, i, pj)
                if P is None:
                    return None
            elif listlen == 2:
                P = naked_double(P, i, pj)
                if P is None:
                    return None
    for j in range(9):
        if j != pj and value in P[pi][j]:
            P[pi][j].remove(value)
            listlen = len(P[pi][j])
            if listlen == 0:
                return None
            elif listlen == 1:
                P = naked_single(P, pi, j)
                if P is None:
                    return None
            elif listlen == 2:
                P = naked_double(P, pi, j)
                if P is None:
                    return None
    for i in range(pi-(pi%3), pi-(pi%3)+3):
        for j in range(pj-(pj%3), pj-(pj%3)+3):
            if not (i == pi and j == pj) and value in P[i][j]:
                P[i][j].remove(value)
                listlen = len(P[i][j])
                if listlen == 0:
                    return None
                elif listlen == 1:
                    P = naked_single(P, i, j)
                    if P is None:
                        return None
                elif listlen == 2:
                    P = naked_double(P, i, j)
                    if P is None:
                        return None
    return P

def naked_double(P, pi, pj):
    value = P[pi][pj]
    for i in range(9):
        if i != pi and value == P[i][pj]:
            for ii in range(9):
                if ii != pi and ii != i and any([x in value for x in P[ii][pj]]):
                    for v in value:
                        if v in P[ii][pj]:
                            P[ii][pj].remove(v)
                    listlen = len(P[ii][pj])
                    if listlen == 0:
                        return None
                    elif listlen == 1:
                        P = naked_single(P, ii, pj)
                        if P is None:
                            return None
                    elif listlen == 2:
                        P = naked_double(P, ii, pj)
                        if P is None:
                            return None
    for j in range(9):
        if j != pj and value == P[pi][j]:
            for jj in range(9):
                if jj != pj and jj != j and any([x in value for x in P[pi][jj]]):
                    for v in value:
                        if v in P[pi][jj]:
                            P[pi][jj].remove(v)
                    listlen = len(P[pi][jj])
                    if listlen == 0:
                        return None
                    elif listlen == 1:
                        P = naked_single(P, pi, jj)
                        if P is None:
                            return None
                    elif listlen == 2:
                        P = naked_double(P, pi, jj)
                        if P is None:
                            return None
    for i in range(pi-(pi%3), pi-(pi%3)+3):
        for j in range(pj-(pj%3), pj-(pj%3)+3):
            if not (i == pi and j == pj) and value == P[i][j]:
                for ii in range(pi-(pi%3), pi-(pi%3)+3):
                    for jj in range(pj-(pj%3), pj-(pj%3)+3):
                        if ii != pi and ii != i and jj != pj and jj != j and any([x in value for x in P[ii][jj]]):
                            for v in value:
                                if v in P[ii][jj]:
                                    P[ii][jj].remove(v)
                            listlen = len(P[ii][jj])
                            if listlen == 0:
                                return None
                            elif listlen == 1:
                                P = naked_single(P, ii, jj)
                                if P is None:
                                    return None
                            elif listlen == 2:
                                P = naked_double(P, ii, jj)
                                if P is None:
                                    return None
    return P

def hidden_single_killer(P):
    from collections import Counter
    for i in range(9):
        candidates = [k for k,v in Counter([p for j in range(9) for p in P[i][j] if len(P[i][j]) > 1]).items() if v == 1]
        for c in candidates:
            j = [j for j in range(9) if c in P[i][j]][0]
            P[i][j] = [c]
            P = naked_single(P, i, j)
            if P is None:
                raise ValueError
    for j in range(9):
        candidates = [k for k,v in Counter([p for i in range(9) for p in P[i][j] if len(P[i][j]) > 1]).items() if v == 1]
        for c in candidates:
            i = [i for i in range(9) if c in P[i][j]][0]
            P[i][j] = [c]
            P = naked_single(P, i, j)
            if P is None:
                raise ValueError
    return P

def is_solved(P):
    return all([len(P[i][j]) == 1 for i in range(9) for j in range(9)])

def recursive(P):
    solutions = []
    for i in range(9):
        for j in range(9):
            if len(P[i][j]) > 1:
                for p in P[i][j]:
                    Pij = deepcopy(P)
                    Pij[i][j] = [p]
                    Pij = naked_single(Pij, i, j)
                    if Pij is not None:
                        if is_solved(Pij):
                            solutions.append(Pij)
                        else:
                            solutions.extend(recursive(Pij))
                return solutions

def puzzle_to_P(puzzle):    
    # initialize probability matrix
    p0 = [i for i in range(1,10)]
    P = [[p0.copy() for i in range(0,9)] for j in range(0,9)]
    
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                P[i][j] = [puzzle[i][j]]
                P = naked_single(P, i, j)
                if P is None:
                    raise ValueError
    return P

def P_to_puzzle(P):
    return [[P[i][j][0] for j in range(9)] for i in range(9)]

def check_puzzle(puzzle):
    # check if values and dimensions valid
    if len(puzzle) != 9 or any([len(puzzle[i]) != 9 for i in range(9)]) or any([not isinstance(puzzle[i][j], int) or puzzle[i][j] not in range(10) for i in range(9) for j in range(9)]):
        raise ValueError

def solve(puzzle):
    """return the solved puzzle as a 2d array of 9 x 9"""
    
    check_puzzle(puzzle)
    P = puzzle_to_P(puzzle)    
    P = hidden_single_killer(P)

    
    if is_solved(P):
        return P_to_puzzle(P)
    
    sudoku_print(P)
    solutions = recursive(P) 
    return P_to_puzzle(solutions[0])
