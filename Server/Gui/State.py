import enum

class State(enum.Enum):
    Connect = 0
    Connecting = 1
    Actions = 2
    FlyingOperations = 3