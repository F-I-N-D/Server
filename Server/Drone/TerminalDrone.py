from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFAULT_RATE, DEFUALT_MASTER

class TerminalDrone(Drone):
    def __init__(self, droneId: str, color: str, master: bool = DEFUALT_MASTER):
        super().__init__(droneId, color, master)

    def connect(self) -> None:
        print('Connecting...')

    def isConnected(self) -> None:
        print('Connected')
        return True

    def disconnect(self) -> None:
        print('Disconnected')

    def kill(self) -> None:
        print('Killed...')

    def addLogger(self) -> None:
        pass

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        self.isFlying = True
        print('Taking off...')

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Landing...')

    def stop(self) -> None:
        if self.isFlying:
            print('Hovering...')

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Moving up...')

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Moving down...')

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Moving forward...')

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Moving backwards...')

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Moving left...')

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Moving right...')

    def turnLeft(self, rate: float = DEFAULT_RATE) -> None:
        if self.isFlying:
            print('Turning left...')

    def turnRight(self, rate: float = DEFAULT_RATE) -> None:
        if self.isFlying:
            print('Turning right...')