import enum

# Enum for the level of the logger
class Level(enum.Enum):
    Debug = 0
    Info = 1
    Warning = 2
    Error = 3
    Critical = 4

    # Make it able to use greather then or equal (>=) between level enums
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    # Make it able to use greather then (>) between level enums
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    # Make it able to use les then or equal (<=) between level enums
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    # Make it able to use les then (<) between level enums
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented