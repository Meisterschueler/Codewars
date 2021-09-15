from itertools import permutations

# store pathes and the blocking character
blocks = {'AC': 'B', 'AI': 'E', 'AG': 'D',
          'BH': 'E',
          'CA': 'B', 'CG': 'E', 'CI': 'F',
          'DF': 'E',
          'FD': 'E',
          'GA': 'D', 'GC': 'E', 'GI': 'H',
          'HB': 'E',
          'IA': 'E', 'IC': 'F', 'IG': 'H'}

def is_valid(path):
    return any([k for k in blocks.keys() if path.find(k) >= 0 and blocks[k] not in path[0:path.find(k)]]) == False

def count_patterns_from(firstPoint, length):
    return 0 if length == 0 else len([path for path in permutations('ABCDEFGHI', length) if path[0] == firstPoint and is_valid(''.join(path))])
