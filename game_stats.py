# game_stats.py

# -------- GAME STATS MODULE --------

def calculate_accuracy(hits, total):
    """
    Returns the accuracy percentage.
    """
    if total == 0:
        return 0
    return round((hits / total) * 100, 2)


def calculate_reaction_stats(reaction_times):
    """
    Returns average, best, and worst reaction times in ms.
    """
    if not reaction_times:
        return 0, 0, 0

    avg = sum(reaction_times) / len(reaction_times)
    best = min(reaction_times)
    worst = max(reaction_times)

    return round(avg, 1), round(best, 1), round(worst, 1)


def get_rank(score):
    """
    Determines rank based on score.
    """
    if score >= 500:
        return "Legend"
    elif score >= 400:
        return "Master"
    elif score >= 300:
        return "Diamond"
    elif score >= 200:
        return "Platinum"
    elif score >= 100:
        return "Gold"
    else:
        return "Silver"