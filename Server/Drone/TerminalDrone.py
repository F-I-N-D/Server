from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFAULT_RATE, DEFUALT_MASTER
from Server.Logger.Logger import Logger

class TerminalDrone(Drone):
    def __init__(self, droneId: str, logger: Logger, color: str, master: bool = DEFUALT_MASTER):
        super().__init__(droneId, logger, color, master)

    def connect(self) -> None:
        super().connect()
        print('Connecting...')

    def isConnected(self) -> None:
        super().isConnected()
        print('Connected')
        return True

    def disconnect(self) -> None:
        super().disconnect()
        print('Disconnected')

    def kill(self) -> None:
        super().kill()
        print('Killed...')

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        super().takeOff()
        self.isFlying = True
        print('Taking off...')

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().land()
        if self.isFlying:
            print('Landing...')

    def stop(self) -> None:
        super().stop()
        if self.isFlying:
            print('Hovering...')

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().up()
        if self.isFlying:
            print('Moving up...')

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().down()
        if self.isFlying:
            print('Moving down...')

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().forward()
        if self.isFlying:
            print('Moving forward...')

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().backward()
        if self.isFlying:
            print('Moving backwards...')

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().left()
        if self.isFlying:
            print('Moving left...')

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().right()
        if self.isFlying:
            print('Moving right...')

    def turnLeft(self, rate: float = DEFAULT_RATE) -> None:
        super().turnLeft()
        if self.isFlying:
            print('Turning left...')

    def turnRight(self, rate: float = DEFAULT_RATE) -> None:
        super().turnRight()
        if self.isFlying:
            print('Turning right...')