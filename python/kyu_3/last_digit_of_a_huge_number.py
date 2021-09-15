def last_digit(lst, rec=False):
    if len(lst) == 0:
        result = [1]
    if len(lst) == 1:
        result = lst
    elif len(lst) == 2:
        d1 = lst[-2]
        d2 = lst[-1]
        if (d1,d2) == (0,0):
            result = [1]
        elif d1 == 0:
            result = [0]
        elif d2 == 0:
            result = [1]
        else:
            if d1 >= 2:
                d1 = d1 % 100
                if d1 <= 1:
                    d1 += 100
      
            if d2 >= 2:
                d2 = d2 % 20
                if d2 <= 1:
                    d2 += 20
            
            result = [d1**d2]

    elif len(lst) > 2:
        rest = lst[0:-2]
        d1 = lst[-2]
        d2 = lst[-1]
        result = last_digit(rest + last_digit([d1, d2], rec=True), rec=True)
    
    return result if rec else result[0] % 10
