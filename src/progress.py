"""Progress track system from Solo Wanderer / Ironsworn style."""

class ProgressTrack:
    def __init__(self, goal_name, difficulty="Normal"):
        self.goal_name = goal_name
        self.difficulty = difficulty
        self.boxes = 10
        self.filled = 0
        self.mark_amounts = {
            "Simple": 3,
            "Easy": 2,
            "Normal": 1,
            "Hard": 0.5,
            "Extreme": 0.25,
        }

    def mark_progress(self, amount=None):
        if amount is None:
            amount = self.mark_amounts.get(self.difficulty, 1)
        self.filled = min(self.boxes, self.filled + amount)
        return self.filled

    def progress_percent(self):
        return (self.filled / self.boxes) * 100

    def is_complete(self):
        return self.filled >= self.boxes

    def reset(self):
        self.filled = 0

    def __str__(self):
        filled_boxes = int(self.filled)
        return f"[{ '#' * filled_boxes }{ '.' * (self.boxes - filled_boxes) }] {self.filled:.1f}/10 ({self.difficulty})"
