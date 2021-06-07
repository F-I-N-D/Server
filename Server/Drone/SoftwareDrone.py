from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFAULT_RATE, DEFUALT_MASTER
from Server.Logger.Logger import Logger

class SoftwareDrone(Drone):
    def __init__(self, droneId: str, logger: Logger, colorFront: str, colorBack: str, master: bool = DEFUALT_MASTER):
        super().__init__(droneId, logger, colorFront, colorBack, master)
        self.connected = False
        self.enableConnect = False

        self.velocityX = 0
        self.velocityY = 0
        self.rate = 0

    def connect(self) -> None:
        super().connect()
        self.enableConnect = True

    def isConnected(self) -> bool:
        super().isConnected()
        return self.connected

    def disconnect(self) -> None:
        super().disconnect()

    def kill(self, message: str) -> None:
        super().kill(message)
        self.velocityX = 0
        self.velocityY = 0
        self.velocityZ = 0
        self.rate = 0
        self.isFlying = False
        self.connected = False

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        super().takeOff(height, velocity)
        self.isFlying = True
        self.locationZ = height

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().land(velocity)
        velocityX = 0
        velocityY = 0
        velocityZ = 0
        newRate = 0
        self.isFlying = False

    def stop(self) -> None:
        super().stop()
        velocityX = 0
        velocityY = 0
        velocityZ = 0
        newRate = 0

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
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.velocityZ = velocityZ
        self.rate = rate
