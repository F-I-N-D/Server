import socket
import time
import json
from threading import Thread
from Server.Drone.Drone import Drone
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone

ADJUSTABLE_VARIABLES = [
    "batteryVoltage",
    "isCharging",
    "isFlying",
    "isTumbled",
    "locationX",
    "locationY",
    "locationZ",
    "direction",
    "distanceDown",
    "distanceFront",
    "distanceBack",
    "distanceLeft",
    "distanceRight",
    "ldr"
]

class Socket(Thread):
    def __init__(self, port: int):
        Thread.__init__(self)
        self.__isRunnning = False
        self.softwareDrones = []
        self.hardwareDrones = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))
        self.clientConnected = False

    def stop(self) -> None:
        self.__isRunnning = False
        self.socket.close()

    def addHardwareDrone(self, drone: HardwareDrone) -> None:
        self.hardwareDrones.append(drone)

    def addSoftwareDrone(self, drone: SoftwareDrone) -> None:
        self.softwareDrones.append(drone)

    def run(self):
        self.__isRunnning = True
        self.socket.listen(1)
        while self.__isRunnning:
            while not self.clientConnected:
                client, address = self.socket.accept()
                self.clientConnected = True

            try:
                request = json.loads(client.recv(1024).decode("utf-8"))
                if request["command"] == "getSoftwareDrones":
                    jsonObject = []
                    for drone in self.softwareDrones:
                        jsonObject.append(self.getDroneData(drone))
                    self.sendResponse(client, jsonObject)
                elif request["command"] == "getHardwareDrones":
                    jsonObject = []
                    for drone in self.hardwareDrones:
                        jsonObject.append(self.getDroneData(drone))
                    self.sendResponse(client, jsonObject)
                elif request["command"] == "connectSoftwareDrone":
                    droneId = request["droneId"]
                    drone = self.getSoftwareDrone(droneId)

                    if drone:
                        if drone.enableConnect:
                            drone.connected = True
                            self.sendResponse(client, { "connected": True })
                        else:
                            self.sendError(client, "notConnecting")
                    else:
                        self.sendError(client, "invalidDrone")
                elif request["command"] == "getSoftwareDroneVelocity":
                    droneId = request["droneId"]
                    drone = self.getSoftwareDrone(droneId)

                    if drone:
                        returnValue = {
                            "droneId": droneId,
                            "velocityX": drone.velocityX,
                            "velocityY": drone.velocityY,
                            "velocityZ": drone.velocityZ,
                            "rate": drone.rate
                        }

                        self.sendResponse(client, returnValue)
                    else:
                        self.sendError(client, "invalidDrone")
                elif request["command"] == "setSoftwareDrone":
                    droneId = request["droneId"]
                    newData = request["data"]
                    
                    drone = self.getSoftwareDrone(droneId)

                    valid = True
                    for newVariableName in newData:
                        if (newVariableName not in ADJUSTABLE_VARIABLES):
                            valid = False

                    if valid and drone:
                        for newVariableName in newData:
                            if newVariableName == "batteryVoltage":
                                drone.batteryVoltage = newData[newVariableName]
                            elif newVariableName == "isCharging":
                                drone.isCharging = newData[newVariableName]
                            elif newVariableName == "isFlying":
                                drone.isFlying = newData[newVariableName]
                            elif newVariableName == "isTumbled":
                                drone.isTumbled = newData[newVariableName]
                            elif newVariableName == "locationX":
                                drone.locationX = newData[newVariableName]
                            elif newVariableName == "locationY":
                                drone.locationY = newData[newVariableName]
                            elif newVariableName == "locationZ":
                                drone.locationZ = newData[newVariableName]
                            elif newVariableName == "direction":
                                drone.direction = newData[newVariableName]
                            elif newVariableName == "distanceDown":
                                drone.distanceDown = newData[newVariableName]
                            elif newVariableName == "distanceFront" and drone.master:
                                drone.distanceFront = newData[newVariableName]
                            elif newVariableName == "distanceBack" and drone.master:
                                drone.distanceBack = newData[newVariableName]
                            elif newVariableName == "distanceLeft" and drone.master:
                                drone.distanceLeft = newData[newVariableName]
                            elif newVariableName == "distanceRight" and drone.master:
                                drone.distanceRight = newData[newVariableName]
                            elif newVariableName == "ldr":
                                drone.ldr = newData[newVariableName]
                        self.sendResponse(client, { "set": True })
                    else:
                        self.sendError(client, "invalidDrone")
                else:
                    self.sendError(client, "invalidCommand")
            except Exception as e:
                self.clientConnected = False
            
    def getSoftwareDrone(self, droneId: str) -> Drone:
        currentDrone = None

        for drone in self.softwareDrones:
            if drone.droneId == droneId:
                currentDrone = drone

        return currentDrone

    def sendResponse(self, client, dataObject: object) -> None:
        client.sendall(bytes(json.dumps(dataObject), "utf-8"))

    def sendError(self, client, message: str) -> None:
        client.sendall(bytes(json.dumps({ "error": message }), "utf-8"))

    @staticmethod
    def getDroneData(drone: HardwareDrone) -> object:
        return {
            "droneId": drone.droneId,
            "master": drone.master,
            "batteryVoltage": drone.batteryVoltage,
            "isCharging": drone.isCharging,
            "isFlying": drone.isFlying,
            "isTumbled": drone.isTumbled,
            "locationX": drone.locationX,
            "locationY": drone.locationY,
            "locationZ": drone.locationZ,
            "direction": drone.direction,
            "distanceDown": drone.distanceDown,
            "distanceFront": drone.distanceFront,
            "distanceBack": drone.distanceBack,
            "distanceLeft": drone.distanceLeft,
            "distanceRight": drone.distanceRight,
            "ldr": drone.ldr,
            "ldrMax": drone.ldrMax,
            "colorFront": drone.colorFront,
            "colorBack": drone.colorBack
        }