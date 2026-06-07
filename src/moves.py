"""Solo Wanderer Moves adapted for sci-fi / Perilous Void context.

Each move function takes game state or relevant params and returns a result dict
with narrative text, progress change, AP change, and any oracle triggers.
"""

from oracles import get_complication, get_peril, get_opportunity
from dice import resolve_test, gain_ap_on_test

def progress_move(target_number, current_ap, advantage=False, disadvantage=False):
    """Catch all for actions that advance a goal: investigate, negotiate, repair, etc."""
    result = resolve_test(target_number, advantage, disadvantage)
    ap_gain = gain_ap_on_test(result)
    narrative = ""
    progress_mark = 0
    peril = None
    complication = None

    if result["outcome"] == "Major":
        narrative = "You discover something helpful or specific to your needs."
        progress_mark = 1
    elif result["outcome"] == "Minor":
        narrative = "You discover something that complicates your goals or introduces a new challenge."
        complication = get_complication()
        ap_gain += 1
    else:
        narrative = "You discover something that poses a threat or unwelcome truth."
        peril = get_peril()

    if result["critical_failure"]:
        peril = get_peril()

    return {
        "move": "Progress",
        "test_result": result,
        "narrative": narrative,
        "progress_mark": progress_mark,
        "ap_change": ap_gain,
        "complication": complication,
        "peril": peril,
    }

def travel_move(target_number, current_ap, advantage=False, disadvantage=False):
    """Travel on foot, by vehicle, or in group. Use appropriate stat + skill TN."""
    result = resolve_test(target_number, advantage, disadvantage)
    ap_gain = gain_ap_on_test(result)
    narrative = ""
    progress_mark = 0
    peril = None
    complication = None

    if result["outcome"] == "Major":
        narrative = "You reach a waypoint. New developments or a safe pause."
        progress_mark = 1
    elif result["outcome"] == "Minor":
        narrative = "You reach a waypoint but face a setback."
        progress_mark = 1
        ap_gain -= 1
        complication = get_complication()
    else:
        narrative = "Complication during travel."
        complication = get_complication()

    if result["critical_failure"]:
        peril = get_peril()

    return {
        "move": "Travel",
        "test_result": result,
        "narrative": narrative,
        "progress_mark": progress_mark,
        "ap_change": ap_gain,
        "complication": complication,
        "peril": peril,
    }

def arrive_move(target_number=3):
    """Upon arriving at destination. Luck based test."""
    result = resolve_test(target_number)
    ap_gain = gain_ap_on_test(result)
    narrative = ""
    progress_mark = 0
    peril = None

    if result["outcome"] == "Major":
        narrative = "The situation favors you upon arrival."
        ap_gain += 1
        progress_mark = 1
    elif result["outcome"] == "Minor":
        narrative = "You arrive to unforeseen challenges."
        peril = get_peril()
    else:
        narrative = "You are lost or misled about the destination."

    if result["critical_failure"]:
        peril = get_peril()

    return {
        "move": "Arrive",
        "test_result": result,
        "narrative": narrative,
        "progress_mark": progress_mark,
        "ap_change": ap_gain,
        "peril": peril,
    }

def scavenge_move(target_number, current_ap, advantage=False, disadvantage=False):
    """Search for loot in wasteland, derelict, ruin, etc."""
    result = resolve_test(target_number, advantage, disadvantage)
    ap_gain = gain_ap_on_test(result)
    narrative = ""
    loot = 0
    peril = None
    complication = None

    if result["outcome"] == "Major":
        narrative = "You find useful loot."
        loot = 2
        ap_gain += 1
    elif result["outcome"] == "Minor":
        narrative = "You find some loot but something happens."
        loot = 1
        peril = get_peril()
    else:
        narrative = "You find nothing and a complication occurs."
        complication = get_complication()
        ap_gain += 1

    if result["critical_failure"]:
        peril = get_peril()

    return {
        "move": "Scavenge",
        "test_result": result,
        "narrative": narrative,
        "loot": loot,
        "ap_change": ap_gain,
        "complication": complication,
        "peril": peril,
    }

def explore_move(target_number, luck_points_spent=0, advantage=False, disadvantage=False):
    """Explore a location. Pay Luck to increase TN."""
    effective_tn = target_number + luck_points_spent
    result = resolve_test(effective_tn, advantage, disadvantage)
    ap_gain = gain_ap_on_test(result)
    narrative = ""
    progress_mark = 0
    peril = None
    complication = None

    if result["outcome"] == "Major":
        narrative = "You find progress toward your goal."
        progress_mark = 1
        ap_gain += 1
    elif result["outcome"] == "Minor":
        narrative = "You uncover a complication at a waypoint."
        complication = get_complication()
    else:
        narrative = "You uncover a peril."
        peril = get_peril()

    if result["critical_failure"]:
        peril = get_peril()

    return {
        "move": "Explore",
        "test_result": result,
        "narrative": narrative,
        "progress_mark": progress_mark,
        "ap_change": ap_gain,
        "complication": complication,
        "peril": peril,
    }

def complete_goal_test(goal_difficulty, current_progress_filled, relevant_stat_tn):
    """Test to finish goal. TN = relevant stat/skill + current filled boxes."""
    tn = relevant_stat_tn + current_progress_filled
    result = resolve_test(tn)

    if result["outcome"] == "Major":
        narrative = "Goal complete. Gain experience."
        xp = 10
    elif result["outcome"] == "Minor":
        narrative = "More work remains or goal twisted. Set new goal one difficulty lower."
        xp = 5
    else:
        narrative = "Goal undone. Remove from tracker."
        xp = 5

    return {
        "move": "Complete Goal",
        "test_result": result,
        "narrative": narrative,
        "xp_gain": xp,
        "success": result["outcome"] == "Major",
    }
