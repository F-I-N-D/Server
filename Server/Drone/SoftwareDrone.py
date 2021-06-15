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

    def dataCallback(self, data) -> None:
        for variableName in data:
            if variableName == "batteryVoltage":
                self.batteryVoltage = data[variableName]
            elif variableName == "isCharging":
                self.isCharging = data[variableName]
            elif variableName == "isFlying":
                self.isFlying = data[variableName]
            elif variableName == "isTumbled":
                self.isTumbled = data[variableName]
            elif variableName == "locationX":
                self.locationX = data[variableName]
            elif variableName == "locationY":
                self.locationY = data[variableName]
            elif variableName == "direction":
                self.direction = data[variableName]
            elif variableName == "distanceDown":
                self.distanceDown = data[variableName]
            elif variableName == "distanceFront" and self.master:
                self.distanceFront = data[variableName]
            elif variableName == "distanceBack" and self.master:
                self.distanceBack = data[variableName]
            elif variableName == "distanceLeft" and self.master:
                self.distanceLeft = data[variableName]
            elif variableName == "distanceRight" and self.master:
                self.distanceRight = data[variableName]
            elif variableName == "ldr":
                self.ldr = data[variableName]

        super().dataCallback(data)

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> bool:
        if not super().takeOff(height, velocity):
            return False
        self.isFlying = True
        self.locationZ = height
        return True

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

    def move(self, velocityX: float, velocityY: float, velocityZ: float, rate: float) -> None:
        super().move(velocityX, velocityY, velocityZ, rate)
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.velocityZ = velocityZ
        self.rate = rate
