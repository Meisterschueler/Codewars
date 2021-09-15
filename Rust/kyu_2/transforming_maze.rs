from copy import deepcopy

gaps = {
    'E': ( 0,  1, 0b0001, 0b0100),
    'S': ( 1,  0, 0b0010, 0b1000),
    'W': ( 0, -1, 0b0100, 0b0001),
    'N': (-1,  0, 0b1000, 0b0010)
}

def rotate_maze(maze):
    return [[e if e in ('B', 'X') else ((e << 1) % 16) + e // 8 for e in row] for row in maze]

def print_maze(ar):
    print('\n'.join([' '.join([str(e).rjust(2) if isinstance(e, int) else " " + e for e in line]) for line in ar]) + '\n')

def print_solutions(ar):
    print('\n'.join([str(list) for list in ar]) + '\n')

def update_solutions_ij(maze, solutions, iteration, i, j, solution_string=None):
    if maze[i][j] == 'X':
        raise ValueError(solutions[i][j])
    
    for direction, (delta_i, delta_j, gap_from, gap_to) in gaps.items():
        (i2, j2) = (i + delta_i, j + delta_j)
        
        if not (0 <= i2 < len(maze)) or not (0 <= j2 < len(maze[0])):
            continue    # i2 or j2 would be out of bounds
        
        if solutions[i2][j2] is not None:
            continue    # already been there            

        if (maze[i][j] != 'B' and maze[i][j] & gap_from != 0):
            continue    # (i,j) -> (i2,j2): cannot leave source
            
        if (maze[i2][j2] != 'X' and maze[i2][j2] & gap_to != 0):
            continue    # (i,j) -> (i2,j2): cannot enter target
                  
        solutions[i2][j2] = deepcopy(solutions[i][j])
        solutions[i2][j2][-1] += direction
                    
        solution_string = solution_string + direction if solution_string else direction
        solutions = update_solutions_ij(maze, solutions, iteration, i2, j2, solution_string)
    
    return solutions
    
def update_solutions(maze, solutions, iteration):
    for i, line in enumerate(solutions):
        for j, element in enumerate(line):
            if isinstance(element, list) and len(element) == iteration:
                if len(solutions[i][j]) <= 3 or any([e != '' for e in solutions[i][j][-3:]]):
                    solutions[i][j].append('')
                solutions = update_solutions_ij(maze, solutions, iteration, i, j, solution_string='')
                
                
    return solutions
    
def maze_solver(maze):
    solutions = [[[] if e == 'B' else None for e in row] for row in maze]
    
    try:
        for i in range(100):
            solutions = update_solutions(maze, solutions, iteration=i)
            maze = rotate_maze(maze)
    except ValueError as e:
        return e.args[0]
    
    return None
