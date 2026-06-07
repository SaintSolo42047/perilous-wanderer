"""Dice and test resolution for Solo Wanderer style 2d20 system."""

import random

def roll_d20():
    return random.randint(1, 20)

def roll_2d20():
    return roll_d20(), roll_d20()

def count_successes(die1, die2, target_number):
    """Return number of successes (0, 1, or 2) where die <= target_number."""
    successes = 0
    if die1 <= target_number:
        successes += 1
    if die2 <= target_number:
        successes += 1
    return successes

def is_critical_failure(die1, die2):
    """True if either die is 20 (cannot be rerolled with AP)."""
    return die1 == 20 or die2 == 20

def resolve_test(target_number, advantage=False, disadvantage=False):
    """
    Roll 2d20 (or 3d20 for adv/disadv), return dict with:
    - dice: tuple of results
    - successes: 0, 1, or 2
    - outcome: 'Major', 'Minor', or 'Miss'
    - critical_failure: bool
    """
    if advantage:
        # Roll 3, keep lowest 2
        rolls = sorted([roll_d20() for _ in range(3)])[:2]
        die1, die2 = rolls[0], rolls[1]
    elif disadvantage:
        # Roll 3, keep highest 2
        rolls = sorted([roll_d20() for _ in range(3)], reverse=True)[:2]
        die1, die2 = rolls[0], rolls[1]
    else:
        die1, die2 = roll_2d20()

    successes = count_successes(die1, die2, target_number)
    crit_fail = is_critical_failure(die1, die2)

    if successes == 2:
        outcome = "Major"
    elif successes == 1:
        outcome = "Minor"
    else:
        outcome = "Miss"

    return {
        "dice": (die1, die2),
        "successes": successes,
        "outcome": outcome,
        "critical_failure": crit_fail,
        "target_number": target_number,
    }

def gain_ap_on_test(result):
    """Gain 1 AP if both dice strictly under TN."""
    die1, die2 = result["dice"]
    tn = result["target_number"]
    if die1 < tn and die2 < tn:
        return 1
    return 0
