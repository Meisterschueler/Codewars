import math

def rowsum(n, multiple, loss):
    if n == 1:
        return max(0, n - 1 + multiple - loss)
    
    num_max = max(0, n + (n * multiple) - 1 - loss)
    num_min = max(0, num_max - n)
    
    sum_0_to_num_max = (num_max * (num_max + 1)) // 2
    sum_0_to_num_min = (num_min * (num_min + 1)) // 2

    return sum_0_to_num_max - sum_0_to_num_min
    
def solve(m, n, l):
    (m, n) = (m, n) if m <= n else (n, m)
    if m == 0:
        return 0
    
    min_pow_2 = 2 ** int(math.log2(m))
    max_pow_2 = 2 ** int(math.log2(n))
    max_width = (n // min_pow_2) * min_pow_2
    
    # calculate upper left rectangle
    rowsum_ul = rowsum(max_width, multiple=0, loss=l)
    rectangle_ul = min_pow_2 * rowsum_ul
    
    # calculate upper right rectangle
    rowsum_ur = rowsum(min_pow_2, multiple=(n // min_pow_2), loss=l)
    rectangle_ur = (n - max_width) * rowsum_ur
    
    if m > min_pow_2:
        # calculate lower left rectangle
        if (max_width // min_pow_2) % 2 == 0:
            rowsum_ll = rowsum(max_width, multiple=0, loss=l)
        else:
            rowsum_ll = rowsum(max_width - min_pow_2, multiple=0, loss=l)
            rowsum_ll += rowsum(min_pow_2, multiple=(max_width // min_pow_2), loss=l)
        rectangle_ll = (m - min_pow_2) * rowsum_ll
        
        # calculate lower right rectangle
        factor = (max_width // min_pow_2)
        factor = factor + 1 if factor % 2 == 0 else factor - 1
        offset = min_pow_2 * factor
        rectangle_lr = solve(m - min_pow_2, n - max_width, l=l-offset)
    else:
        rectangle_ll = 0
        rectangle_lr = 0
    
    return rectangle_ul + rectangle_ur + rectangle_ll + rectangle_lr
    
def elder_age(m, n, l, t):
    return solve(m, n, l) % t
