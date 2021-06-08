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
                        drone.dataCallback(newData)
                        self.sendResponse(client, { "set": True })
                    elif not drone:
                        self.sendError(client, "invalidDrone")
                    elif not valid:
                        self.sendError(client, "invalidData")
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