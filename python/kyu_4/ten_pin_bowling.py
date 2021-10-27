def bowling_score(frames):
    rolls = []
    for idx, frame in enumerate(frames.split(' ')):
        for roll in frame:
            if roll.isdigit():
                rolls.append(('d', int(roll), idx == 9))
            elif roll == 'X':
                rolls.append(('X', 10, idx == 9))
            elif roll == '/':
                rolls.append(('/', 10 - rolls[-1][1], idx == 9))
    
    total_scores = 0
    for idx, (command, scores, last_round) in enumerate(rolls):
        if command == 'd':
            total_scores += scores
        elif command == 'X':
            total_scores += 10
            if not last_round:
                total_scores += rolls[idx+1][1] + rolls[idx+2][1]
        elif command == '/':
            total_scores += scores
            if not last_round:
                total_scores += rolls[idx+1][1]

    return total_scores
