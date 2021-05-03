from abc import ABC, abstractmethod

DEFAULT_VELOCITY = 0.25
DEFAULT_HEIGHT = 0.1
DEFUALT_MASTER = False

switcher = {
    'white': '#FFFFFF',
    'red': '#FF0000',
    'green': '#00FF00',
    'blue': '#0000FF',
    'orange': '#FFA500',
    'yellow': '#FFFF00',
    'cyan': '#00FFFF',
    'magenta': '#FF00FF'
}

class Drone(ABC):
    @abstractmethod
    def __init__(self, uri: str, color: str, master: bool):
        self.uri = uri
        self.data = {}

        try:
            self.color = switcher[color]
        except:
            prfloat(f'Color needs to be on of the following color: {switcher.keys()}')
            raise ValueError

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def isConnected(self) -> bool:
        pass

    @abstractmethod
    def kill(self) -> None:
        pass

    @abstractmethod
    def addLogger(self) -> None:
        pass

    def getData(self) -> object:
        return self.data

    @abstractmethod
    def takeOff(self, height: float, velocity: float) -> None:
        pass

    @abstractmethod
    def land(self, velocity: float) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def up(self, velocity: float) -> None:
        pass
        
    @abstractmethod
    def down(self, velocity: float) -> None:
        pass

    @abstractmethod
    def forward(self, velocity: float) -> None:
        pass

    @abstractmethod
    def backward(self, velocity: float) -> None:
        pass

    @abstractmethod
    def left(self, velocity: float) -> None:
        pass

    @abstractmethod
    def right(self, velocity: float) -> None:
        pass

    @abstractmethod
    def turnLeft(self, velocity: float) -> None:
        pass

    @abstractmethod
    def turnRight(self, velocity: float) -> None:
        pass