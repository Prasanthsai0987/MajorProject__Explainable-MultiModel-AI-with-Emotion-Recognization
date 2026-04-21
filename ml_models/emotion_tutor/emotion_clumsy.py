import time
from collections import defaultdict, deque

class EmotionTracker:
    def __init__(self):
        self.last_emotion = None
        self.last_time = time.time()
        self.duration = defaultdict(float)
        self.changes = deque()

    def update(self, emotion):
        now = time.time()

        if self.last_emotion:
            self.duration[self.last_emotion] += now - self.last_time

        if emotion != self.last_emotion:
            self.changes.append(now)

        self.last_emotion = emotion
        self.last_time = now

        # keep only last 1 minute
        while self.changes and now - self.changes[0] > 60:
            self.changes.popleft()

    def summary(self):
        clumsy = len(self.changes) > 3
        return {
            "emotion_durations": {
                k: round(v, 2) for k, v in self.duration.items()
            },
            "clumsy_behavior": clumsy
        }
