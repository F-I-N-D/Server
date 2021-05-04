from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFUALT_MASTER

class TerminalDrone(Drone):
    def __init__(self, id: str, color: str, master: bool = DEFUALT_MASTER):
        super().__init__(id, color, master)

    def connect(self) -> None:
        print('Connecting...')

    def isConnected(self) -> None:
        print('Connected')
        return True

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

    def turnLeft(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Turning left...')

    def turnRight(self, velocity: float = DEFAULT_VELOCITY) -> None:
        if self.isFlying:
            print('Turning right...')