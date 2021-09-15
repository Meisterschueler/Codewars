from itertools import permutations

def solve_puzzle (clues):
    size = 6
    variants = {i: set() for i in range(size+1)}
    for row in permutations(range(1, size+1)):
        visible = sum(v >= max(row[:i+1]) for i, v in enumerate(row))
        variants[visible].add(row)
        variants[0].add(row)
        
    possible_cols, possible_rows = [], []
    for i in range(size):
        clue_left, clue_right = clues[4*size-1-i], clues[size + i]
        var_left = variants[clue_left]
        var_right = set(map(lambda row: tuple(reversed(row)), variants[clue_right]))
        possible_rows.append(var_left.intersection(var_right))

        clue_top, clue_btm = clues[i], clues[3*size-1-i]
        var_top = variants[clue_top]
        var_btm = set(map(lambda row: tuple(reversed(row)), variants[clue_btm]))
        possible_cols.append(var_top.intersection(var_btm))
        
    while any(len(var_row) > 1 for var_row in possible_rows):
        for i in range(size):
            for j in range(size):
                row_set = set(row[j] for row in possible_rows[i])
                col_set = set(col[i] for col in possible_cols[j])
                union_set = row_set.intersection(col_set)
                possible_rows[i] = [row for row in possible_rows[i] if row[j] in union_set]
                possible_cols[j] = [col for col in possible_cols[j] if col[i] in union_set]

    return tuple(row[0] for row in possible_rows)
