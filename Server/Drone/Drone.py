from abc import ABC, abstractmethod
from Server.Logger.Logger import Logger

DEFAULT_VELOCITY = 0.5
DEFAULT_MIN_VELOCITY = 0.1
DEFAULT_RATE = 22
DEFAULT_HEIGHT = 0.4
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
    def __init__(self, droneId: str, logger: Logger, colorFront: str, colorBack: str, master: bool):
        self.droneId = droneId
        self.master = master
        self.logger = logger

        self.batteryVoltage = 0.0
        self.isCharging = False

        self.isFlying = False
        self.isTumbled = False

        self.targetReached = False

        self.locationX = 0
        self.locationY = 0
        self.locationZ = 0
        self.direction = 0

        self.targetLocationX = 0
        self.targetLocationY = 0
        self.targetLocationZ = 0

        self.distanceDown = 0
        self.distanceFront = 0
        self.distanceBack = 0
        self.distanceLeft = 0
        self.distanceRight = 0

        self.ldr = 0
        self.ldrMax = 0

        try:
            self.colorFront = switcher[colorFront]
            self.colorBack = switcher[colorBack]
        except:
            print(f'Color needs to be on of the following color: {switcher.keys()}')
            raise ValueError

    @abstractmethod
    def connect(self) -> None:
        self.logger.info("Connect", self.droneId)

    @abstractmethod
    def isConnected(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        self.logger.info("Disconnect", self.droneId)

    def logData(self) -> None:
        self.logger.info(f"Battery: {self.batteryVoltage}V", self.droneId)
        self.logger.info(f"Is charging: {self.isCharging}", self.droneId)
        self.logger.info(f"Is flying: {self.isFlying}", self.droneId)
        self.logger.info(f"Is tumbled: {self.isTumbled}", self.droneId)
        self.logger.info(f"LDR: {self.ldr}", self.droneId)

        self.logger.info(f"Distance down: {self.distanceDown}", self.droneId)
        
        if self.master:
            self.logger.info(f"Distance front: {self.distanceFront}", self.droneId)
            self.logger.info(f"Distance back: {self.distanceBack}", self.droneId)
            self.logger.info(f"Distance left: {self.distanceLeft}", self.droneId)
            self.logger.info(f"Distance right: {self.distanceRight}", self.droneId)

        self.logger.info(f"x: {self.locationX}", self.droneId)
        self.logger.info(f"y: {self.locationY}", self.droneId)
        self.logger.info(f"z: {self.locationZ}", self.droneId)
        self.logger.info(f"direction: {self.direction}", self.droneId)

    @abstractmethod
    def kill(self) -> None:
        self.logger.critical("Killed", self.droneId)

    @abstractmethod
    def takeOff(self, height: float, velocity: float) -> None:
        self.logger.debug("Taking off", self.droneId)

    @abstractmethod
    def land(self, velocity: float) -> None:
        self.logger.debug("Landing", self.droneId)

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
    def turnLeft(self, rate: float) -> None:
        pass

    @abstractmethod
    def turnRight(self, rate: float) -> None:
        pass

    @abstractmethod
    def move(self, velocityX: float, velocityY: float, velocityZ: float, rate: float) -> None:
        pass

    def adjust(self, velocity: float = DEFAULT_VELOCITY, minVelocity: float = DEFAULT_MIN_VELOCITY, rate: float = DEFAULT_RATE):
        differenceX = self.targetLocationX - self.locationX
        differenceY = self.targetLocationY - self.locationY
        differenceZ = self.targetLocationZ - self.locationZ

        differenceZ = 0
        self.targetReached = abs(differenceX) < 25 and abs(differenceY) < 25 and abs(differenceZ) < 7

        velocityX = 0
        velocityY = 0
        velocityZ = 0
        newRate = 0

        if -25 < self.direction < 25:
            if -100 < differenceX < -20:
                velocityX = velocity / (100 - abs(differenceX))
                if velocityX < DEFAULT_MIN_VELOCITY:
                    velocityX = DEFAULT_MIN_VELOCITY
            elif 20 < differenceX < 100:
                velocityX = -velocity / (100 - abs(differenceX))
                if velocityX > -DEFAULT_MIN_VELOCITY:
                    velocityX = -DEFAULT_MIN_VELOCITY
            elif differenceX < -20 or differenceX > 20:
                if differenceX < 0:
                    velocityX = velocity
                elif differenceX > 0:
                    velocityX = -velocity


            if -100 < differenceY < -20:
                velocityY = -velocity / (100 - abs(differenceY))
                if velocityY > -DEFAULT_MIN_VELOCITY:
                    velocityY = -DEFAULT_MIN_VELOCITY
            elif 20 < differenceY < 100:
                velocityY = velocity / (100 - abs(differenceY))
                if velocityY < DEFAULT_MIN_VELOCITY:
                    velocityY = DEFAULT_MIN_VELOCITY
            elif differenceY < -20 or differenceY > 20:
                if differenceY < 0:
                    velocityY = -velocity
                elif differenceY > 0:
                    velocityY = velocity

        if -50 < differenceZ < -5:
            velocityZ = -velocity / (50 - abs(differenceZ))
            if velocityZ > -DEFAULT_MIN_VELOCITY:
                velocityZ = -DEFAULT_MIN_VELOCITY
        elif 5 < differenceZ < 50:
            velocityZ = velocity / (50 - abs(differenceZ))
            if velocityZ > DEFAULT_MIN_VELOCITY:
                velocityZ = DEFAULT_MIN_VELOCITY
        elif differenceZ < -5 or differenceZ > 5:
            if differenceZ < 0:
                velocityZ = -velocity
            elif differenceZ > 0:
                velocityZ = velocity

        if self.direction > 10:
            newRate = -rate
        elif self.direction < -10:
            newRate = rate

        self.move(velocityX, velocityY, 0, newRate)

    def setTarget(self, targetLocationX, targetLocationY, targetLocationZ):
        self.targetLocationX = targetLocationX
        self.targetLocationY = targetLocationY
        self.targetLocationZ = targetLocationZ