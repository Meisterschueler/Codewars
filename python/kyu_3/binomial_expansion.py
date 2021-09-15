import re
from scipy.special import binom
def expand(expr):
    
    match = re.match(r'\((\+|\-)?(\d+)?([a-z]{1})((\+|\-)(\d+))\)\^(\d+)', expr)
    
    c1 = int(match.group(2)) if match.group(2) else 1
    c1 *= -1 if match.group(1) == '-' else 1
    
    s1 = match.group(3)
    c2 = int(match.group(4))
    expo = int(match.group(7))
    
    result = []
    for ex in range(expo, -1, -1):
        coeff = int(binom(expo,ex) * c1**ex * c2**(expo-ex))
        result.append('{}{}{}{}'.format('+' if coeff > 0 and ex < expo else ('-' if coeff == -1 and ex == expo else ''), coeff if not (abs(coeff) == 1 and ex == expo) else '', s1 if ex != 0 else '', ('^' + str(ex)) if ex > 1 else ''))
        
    result = ''.join(result)
    return result if result != '' else '1'
