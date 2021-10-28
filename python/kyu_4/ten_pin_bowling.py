def bowling_score(frames):
    # calculate scores of each single roll
    rolls = []
    for idx, frame in enumerate(frames.split(' ')):
        last_round = idx == 9
        for roll in frame:
            scores = 10 - rolls[-1][1] if roll == '/' else 10 if roll == 'X' else int(roll)
            rolls.append((roll, scores, last_round))
    
    # calculate total scores with boni because of spares (/) and strikes (X)
    total_scores = 0
    for idx, (roll, scores, last_round) in enumerate(rolls):
        total_scores += scores
        if not last_round:
            if roll == '/':
                total_scores += rolls[idx+1][1]
            elif roll == 'X':
                total_scores += rolls[idx+1][1] + rolls[idx+2][1]

    return total_scores
