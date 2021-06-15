import enum

# Enum for the state of the GUI
class State(enum.Enum):
    Null = None
    Connect = 0
    Connecting = 1
    Actions = 2
    FlyingOperations = 3