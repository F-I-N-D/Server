import enum

# Enum for the goal of the swam
class Goal(enum.Enum):
    Null = None
    Search = 0
    Scatter = 1
    Calibrate = 2
    FollowTarget = 3