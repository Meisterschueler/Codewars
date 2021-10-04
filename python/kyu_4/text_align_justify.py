def justify(text, width):
    # split the words into lines
    word_lines = [[]]
    for word in text.split(' '):
        if sum([len(w) for w in word_lines[-1]]) + len(word_lines[-1]) + len(word) <= width:
            word_lines[-1].append(word)
        else:
            word_lines.append([word])
    
    # join the words (per line)
    lines = []
    for idx,words in enumerate(word_lines):
        if idx == len(word_lines) - 1:
            lines.append(' '.join(words))
        elif len(words) == 1:
            lines.append(words[0])
        else:
            gaps = len(words) - 1
            spaces = width - sum([len(word) for word in words])
            min_space = ' ' * (spaces // gaps)
            spaces_left = spaces % gaps
            line = min_space.join(words)
            line = line.replace(min_space, min_space + ' ', spaces_left)
            lines.append(line)

    # join all lines
    return '\n'.join(lines)
