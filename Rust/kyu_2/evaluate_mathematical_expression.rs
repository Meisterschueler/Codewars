import re

def tokenize(expression):
    expression = expression.replace(' ', '')
    tokens = []
    while len(expression) > 0:
        match_number = re.match(r'^(?P<number>((\d+)(\.\d+)?))(?P<rest>.*)$', expression)
        match_operator = re.match(r'^(?P<operator>(\+|\-|\*|\/|\(|\)))(?P<rest>.*)$', expression)
    
        if match_number:
            tokens.append(float(match_number.group('number')))
            expression = match_number.group('rest')
        elif match_operator:
            tokens.append(match_operator.group('operator'))
            expression = match_operator.group('rest')
        else:
            raise ValueError(expression)
    
    return tokens

def solve(tokens):
    while any([t in ('(',')') for t in tokens]):
        for idx in range(0, len(tokens)):
            if tokens[idx] == '(':
                opening_idx = idx
            if tokens[idx] == ')':
                subtoken = solve(tokens[opening_idx+1:idx])
                tokens = tokens[0:opening_idx] + [subtoken] + tokens[idx+1:]
                return solve(tokens)
            
    if len(tokens) == 1 and isinstance(tokens[0], float):
        return tokens[0]
    elif len(tokens) == 2 and tokens[0] in ('+', '-') and isinstance(tokens[1], float):
        return tokens[1] if tokens[0] == '+' else -tokens[1]
    else:
        if len(tokens) > 2 and tokens[0] in ('+','-') and isinstance(tokens[1], float):
            tokens = tokens[1:] if tokens[0] == '+' else [-tokens[1]] + tokens[2:]
        
        while len(tokens) >= 3 and any([tokens[idx] in ('+','-','*','/') and tokens[idx+1] in ('+','-') for idx in range(0,len(tokens)-2)]):
            for idx in range(0,len(tokens)-2):
                if tokens[idx] in ('+','-','*','/') and tokens[idx+1] in ('+','-') and isinstance(tokens[idx+2], float):
                    tokens = tokens[0:idx+1] + [tokens[idx+2] if tokens[idx+1] == '+' else -tokens[idx+2]] + tokens[idx+3:]
                    break
        
        while any([t in ('*','/') for t in tokens]):
            for idx in range(1, len(tokens)-1):
                if tokens[idx] in ('*','/'):
                    tokens = tokens[0:idx-1] + [tokens[idx-1]*tokens[idx+1] if tokens[idx] == '*' else tokens[idx-1]/tokens[idx+1]] + tokens[idx+2:]
                    break
        
        while any([t in ('+','-') for t in tokens]):
            for idx in range(1, len(tokens)-1):
                if tokens[idx] in ('+','-'):
                    tokens = tokens[0:idx-1] + [tokens[idx-1]+tokens[idx+1] if tokens[idx] == '+' else tokens[idx-1]-tokens[idx+1]] + tokens[idx+2:]
                    break
        
        return tokens[0]

def calc(expression):
    tokens = tokenize(expression)
    return solve(tokens)
