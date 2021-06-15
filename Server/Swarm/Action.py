import enum

# Enum for the action of the swarm
class Action(enum.Enum):
    Null = None
    Connect = 10
    Search = 20
    Calibrate = 21
    Scatter = 22
    Disconnect = 23
    Land = 30
    Kill = 31