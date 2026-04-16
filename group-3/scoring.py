from collections import Counter

def calculate_score(dice):
    """
    Calculates the score for a given list of dice.
    Returns a tuple (score, scoring_dice_count).
    If scoring_dice_count < len(dice), it means some selected dice don't score.
    """
    if not dice:
        return 0, 0
        
    counts = Counter(dice)
    score = 0
    scoring_dice_count = 0
    
    # Check for 6 of a kind
    if any(count == 6 for count in counts.values()):
        return 3000, 6
        
    # Check for Run (1-2-3-4-5-6)
    if len(counts) == 6:
        return 2500, 6
        
    # Check for 3 pair
    if len(counts) == 3 and all(count == 2 for count in counts.values()):
        return 1500, 6
        
    # Check for 5 of a kind
    for face, count in counts.items():
        if count == 5:
            score += 2000
            scoring_dice_count += 5
            counts[face] -= 5
            
    # Check for 4 of a kind
    for face, count in counts.items():
        if count == 4:
            score += 1000
            scoring_dice_count += 4
            counts[face] -= 4
            
    # Check for 3 of a kind
    for face, count in counts.items():
        if count == 3:
            if face == 1:
                score += 1000
            else:
                score += face * 100
            scoring_dice_count += 3
            counts[face] -= 3
            
    # Check for singles
    if counts[1] > 0:
        score += counts[1] * 100
        scoring_dice_count += counts[1]
        counts[1] = 0
        
    if counts[5] > 0:
        score += counts[5] * 50
        scoring_dice_count += counts[5]
        counts[5] = 0
        
    return score, scoring_dice_count

def get_valid_scoring_dice(dice):
    """
    Returns the dice that actually contribute to the score.
    """
    score, count = calculate_score(dice)
    return score > 0 and count == len(dice)

def has_scoring_dice(dice):
    """
    Checks if a roll has any scoring dice (to check for bust).
    """
    counts = Counter(dice)
    if counts[1] > 0 or counts[5] > 0:
        return True
    if any(count >= 3 for count in counts.values()):
        return True
    if len(counts) == 6:
        return True
    if len(counts) == 3 and all(count == 2 for count in counts.values()):
        return True
    return False
