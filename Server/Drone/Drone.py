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

        self.distanceDown = 0
        self.distanceFront = 0
        self.distanceBack = 0
        self.distanceLeft = 0
        self.distanceRight = 0

        self.ldr = 0.0
        self.ldrMax = 0.0

        self.framesNotSeen = 0

        try:
            self.colorFront = switcher[colorFront]
            self.colorBack = switcher[colorBack]
        except:
            raise ValueError(f'Color needs to be on of the following color: {switcher.keys()}')

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
        self.logger.debug(f"Battery: {self.batteryVoltage}V", self.droneId)
        self.logger.debug(f"Is charging: {self.isCharging}", self.droneId)
        self.logger.debug(f"Is flying: {self.isFlying}", self.droneId)
        self.logger.debug(f"Is tumbled: {self.isTumbled}", self.droneId)
        self.logger.debug(f"LDR: {self.ldr}", self.droneId)

        self.logger.debug(f"Distance down: {self.distanceDown}", self.droneId)
        
        if self.master:
            self.logger.debug(f"Distance front: {self.distanceFront}", self.droneId)
            self.logger.debug(f"Distance back: {self.distanceBack}", self.droneId)
            self.logger.debug(f"Distance left: {self.distanceLeft}", self.droneId)
            self.logger.debug(f"Distance right: {self.distanceRight}", self.droneId)

        self.logger.debug(f"x: {self.locationX}", self.droneId)
        self.logger.debug(f"y: {self.locationY}", self.droneId)
        self.logger.debug(f"z: {self.locationZ}", self.droneId)
        self.logger.debug(f"direction: {self.direction}", self.droneId)

    @abstractmethod
    def kill(self, message: str) -> None:
        self.logger.critical(f"Killed: {message}", self.droneId)
        self.logData()

    @abstractmethod
    def dataCallback(self, data) -> None:
        if self.isTumbled:
            self.kill("Tumbled")
        elif self.isCharging:
            self.kill("Charging")

        if self.batteryVoltage < 2.8 and self.batteryVoltage > 0.0:
            self.kill("Battery low", self.droneId)
            self.disconnect()

    @abstractmethod
    def takeOff(self, height: float, velocity: float) -> bool:
        self.logData()
        self.logger.info(f"Taking off to {height}", self.droneId)
        if self.batteryVoltage < 3.5 and self.batteryVoltage > 0.0:
            self.logger.warning("Battery low", self.droneId)
            self.disconnect()
            return False
        return True

    @abstractmethod
    def land(self, velocity: float) -> None:
        self.logger.info("Landing", self.droneId)
        self.logData()

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def move(self, velocityX: float, velocityY: float, velocityZ: float, rate: float) -> None:
        pass

    def adjust(self, velocity: float = DEFAULT_VELOCITY, minVelocity: float = DEFAULT_MIN_VELOCITY, rate: float = DEFAULT_RATE):
        differenceX = self.targetLocationX - self.locationX
        differenceY = self.targetLocationY - self.locationY

        self.targetReached = abs(differenceX) < 25 and abs(differenceY) < 25

        velocityX = 0
        velocityY = 0
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

        if self.direction > 10:
            newRate = -rate
        elif self.direction < -10:
            newRate = rate

        self.move(velocityX, velocityY, 0, newRate)

    def setTarget(self, targetLocationX, targetLocationY):
        self.targetLocationX = targetLocationX
        self.targetLocationY = targetLocationY
