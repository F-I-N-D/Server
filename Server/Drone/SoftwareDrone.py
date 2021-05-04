from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFUALT_MASTER

class SoftwareDrone(Drone):
    def __init__(self, id: str, color: str, master: bool = DEFUALT_MASTER):
        super().__init__(id, color)

    def connect(self) -> None:
        pass

    def isConnected(self) -> bool:
        pass

    def kill(self) -> None:
        pass

    def addLogger(self) -> None:
        pass

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def stop(self) -> None:
        pass

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def turnLeft(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass

    def turnRight(self, velocity: float = DEFAULT_VELOCITY) -> None:
        pass