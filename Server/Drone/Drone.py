from abc import ABC, abstractmethod

from Server.Logger.Logger import Logger

# Constants
DEFAULT_VELOCITY = 0.5
DEFAULT_MIN_VELOCITY = 0.1
DEFAULT_RATE = 22
DEFAULT_HEIGHT = 0.4
DEFUALT_MASTER = False

# Switcher for color conversion
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
        self.logger.debug("Connect", self.droneId)

    @abstractmethod
    def isConnected(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        self.logger.debug("Disconnect", self.droneId)

    # Log all data of the drone
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

    # Kill the drone if it is going to crash
    @abstractmethod
    def kill(self, message: str) -> None:
        self.logger.critical(f"Killed: {message}", self.droneId)
        self.logData()

    # Data callback that runs when data is recieved
    @abstractmethod
    def dataCallback(self, data) -> None:
        if self.isTumbled:
            self.kill("Tumbled")
        elif self.isCharging:
            self.kill("Charging")

        if self.batteryVoltage < 2.8 and self.batteryVoltage > 0.0:
            self.kill("Battery low", self.droneId)
            self.disconnect()

    # Take off if the battery is full enough
    @abstractmethod
    def takeOff(self, height: float, velocity: float) -> bool:
        self.logData()
        self.logger.debug(f"Taking off to {height}", self.droneId)
        if self.batteryVoltage < 3.5 and self.batteryVoltage > 0.0:
            self.logger.warning("Battery low", self.droneId)
            self.disconnect()
            return False
        return True

    @abstractmethod
    def land(self, velocity: float) -> None:
        self.logger.debug("Landing", self.droneId)
        self.logData()

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def move(self, velocityX: float, velocityY: float, velocityZ: float, rate: float) -> None:
        pass

    # Adjust the velocity based on the current location and the target
    def adjust(self, adjustX: float = 0.0, adjustY: float = 0.0, velocity: float = DEFAULT_VELOCITY, minVelocity: float = DEFAULT_MIN_VELOCITY, rate: float = DEFAULT_RATE):
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

        self.move(velocityX + adjustX, velocityY + adjustY, 0, newRate)

    # Set the target of the drone
    def setTarget(self, targetLocationX, targetLocationY):
        self.targetLocationX = targetLocationX
        self.targetLocationY = targetLocationY
