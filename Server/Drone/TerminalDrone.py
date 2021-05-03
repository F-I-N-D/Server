from .Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFUALT_MASTER

class TerminalDrone(Drone):
    def __init__(self, uri: str, color: str, master: bool = DEFUALT_MASTER):
        super().__init__(uri, color, master)

    def connect(self) -> None:
        print("Connecting...")

    def isConnected(self) -> None:
        print("Connected")
        return True

    def kill(self) -> None:
        print("Killed...")

    def addLogger(self) -> None:
        pass

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Taking off...")

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Landing...")

    def stop(self) -> None:
        print("Hovering...")

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Moving up...")

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Moving down...")

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Moving forward...")

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Moving backwards...")

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Moving left...")

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Moving right...")

    def turnLeft(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Turning left...")

    def turnRight(self, velocity: float = DEFAULT_VELOCITY) -> None:
        print("Turning right...")