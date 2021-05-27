from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFAULT_RATE, DEFUALT_MASTER
from Server.Logger.Logger import Logger

class SoftwareDrone(Drone):
    def __init__(self, droneId: str, logger: Logger, colorFront: str, colorBack: str, master: bool = DEFUALT_MASTER):
        super().__init__(droneId, logger, colorFront, colorBack, master)
        self.connected = False

    def connect(self) -> None:
        super().connect()

    def isConnected(self) -> bool:
        super().isConnected()
        return self.connected

    def disconnect(self) -> None:
        super().disconnect()

    def kill(self) -> None:
        super().kill()

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        super().takeOff(height, velocity)

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().land(velocity)

    def stop(self) -> None:
        super().stop()

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().up(velocity)

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().down(velocity)

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().forward(velocity)

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().backward(velocity)

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().left(velocity)

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().right(velocity)

    def turnLeft(self, rate: float = DEFAULT_RATE) -> None:
        super().turnLeft(rate)

    def turnRight(self, rate: float = DEFAULT_RATE) -> None:
        super().turnRight(rate)

    def move(self, velocityX: float, velocityY: float, velocityZ: float, rate: float) -> None:
        super().move(velocityX, velocityY, velocityZ, rate)
