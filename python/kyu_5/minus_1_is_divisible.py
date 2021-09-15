def how_many_times(a, b):
    if a == b:
        return a
    
    if b > a:
        (a,b) = (b,a)   
    
    result = 0
    while b > 0:
        if a % b == 0:
            result += 1

        new_b = int((a-b)/(int(a/b)))
        new_a = a - (b-new_b)
        (a,b) = (new_a, new_b)
    
    return result
