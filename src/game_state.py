"""Simple game state for testing the solo engine."""

from progress import ProgressTrack
from moves import progress_move, travel_move, scavenge_move, explore_move, arrive_move, complete_goal_test
import random

class SimpleCharacter:
    def __init__(self):
        self.luck = 7
        self.survival = 5
        self.perception = 6
        self.charisma = 5
        self.endurance = 6
        self.ap = 3

    def get_tn(self, stat_name):
        stats = {
            "luck": self.luck,
            "survival": self.survival,
            "perception": self.perception,
            "charisma": self.charisma,
            "endurance": self.endurance,
        }
        return stats.get(stat_name.lower(), 5)

class SoloGame:
    def __init__(self, goal_name="Survive the derelict station", difficulty="Normal"):
        self.character = SimpleCharacter()
        self.goal = ProgressTrack(goal_name, difficulty)
        self.current_location = "Unknown derelict corridor"
        self.log = []
        self.active_peril = None

    def add_log(self, text):
        self.log.append(text)
        print(text)

    def perform_move(self, move_name, **kwargs):
        self.add_log(f"\n--- Performing {move_name} ---")
        result = None

        if move_name == "Progress":
            tn = kwargs.get("tn", self.character.get_tn("perception") + 2)
            result = progress_move(tn, self.character.ap)
        elif move_name == "Travel":
            tn = kwargs.get("tn", self.character.get_tn("endurance") + self.character.get_tn("survival"))
            result = travel_move(tn, self.character.ap)
        elif move_name == "Scavenge":
            tn = kwargs.get("tn", self.character.get_tn("luck") + self.character.get_tn("survival"))
            result = scavenge_move(tn, self.character.ap)
        elif move_name == "Explore":
            tn = kwargs.get("tn", self.character.get_tn("luck"))
            result = explore_move(tn, luck_points_spent=kwargs.get("luck_spent", 0))
        elif move_name == "Arrive":
            tn = kwargs.get("tn", self.character.get_tn("luck") + 3)
            result = arrive_move(tn)
        else:
            self.add_log("Unknown move.")
            return

        self.character.ap = max(0, self.character.ap + result.get("ap_change", 0))

        self.add_log(result["narrative"])
        self.add_log(f"Test: {result['test_result']['dice']} vs TN {result['test_result']['target_number']} -> {result['test_result']['outcome']}")
        self.add_log(f"AP now: {self.character.ap}")

        if result.get("progress_mark", 0) > 0:
            self.goal.mark_progress(result["progress_mark"])
            self.add_log(f"Progress: {self.goal}")

        if result.get("complication"):
            self.add_log(f"Complication: {result['complication']}")
        if result.get("peril"):
            self.active_peril = result["peril"]
            self.add_log(f"Peril: {result['peril']}")

        if result["test_result"]["critical_failure"]:
            self.add_log("Critical failure triggered additional peril check.")

        return result

    def spend_ap(self, purpose="reroll"):
        if self.character.ap > 0:
            self.character.ap -= 1
            self.add_log(f"Spent 1 AP for {purpose}. AP remaining: {self.character.ap}")
            return True
        self.add_log("No AP left.")
        return False

    def check_goal_completion(self):
        self.add_log("\n--- Attempting to complete goal ---")
        relevant_tn = self.character.get_tn("charisma")
        result = complete_goal_test(self.goal.difficulty, int(self.goal.filled), relevant_tn)
        self.add_log(result["narrative"])
        if result["success"]:
            self.add_log("Goal achieved!")
            self.goal.reset()
        return result


if __name__ == "__main__":
    game = SoloGame("Investigate the abandoned orbital station", "Normal")
    print("Starting solo session...")
    print(f"Goal: {game.goal.goal_name}")
    print(f"Initial progress: {game.goal}")

    game.perform_move("Explore")
    game.perform_move("Scavenge")
    game.perform_move("Progress", tn=10)
    print("\nCurrent AP:", game.character.ap)
    print("Final progress:", game.goal)
