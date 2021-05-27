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
    "distanceUp",
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
                response = json.loads(client.recv(1024).decode("utf-8"))
        
                if response["command"] == "getSoftwareDrones":
                    jsonObject = []
                    for drone in self.softwareDrones:
                        jsonObject.append(self.getDroneData(drone))
                    client.sendall(bytes(json.dumps(jsonObject), "utf-8"))
                elif response["command"] == "getHardwareDrones":
                    jsonObject = []
                    for drone in self.hardwareDrones:
                        jsonObject.append(self.getDroneData(drone))
                    client.sendall(bytes(json.dumps(jsonObject), "utf-8"))
                elif response["command"] == "connectSoftwareDrone:":
                    droneId = response["droneId"]
                    drone = self.getDrone(droneId)

                    if drone:
                        drone.connected = True
                        client.sendall(b"valid")
                    else:
                        client.sendall(b"invalid")
                elif response["command"] == "setSoftwareDrone:":
                    droneId = response["droneId"]
                    newData = response["data"]
                    
                    drone = self.getDrone(droneId)

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
                            elif newVariableName == "distanceUp" and drone.master:
                                drone.distanceUp = newData[newVariableName]
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

                        client.sendall(b"valid")
                    else:
                        client.sendall(b"invalid")
                else:
                    client.sendall(b"invalidCommand")
            except:
                self.clientConnected = False
            
    def getDrone(self, droneId: str) -> Drone:
        currentDrone = None

        for drone in self.softwareDrones:
            if drone.droneId == droneId:
                currentDrone = drone

        return currentDrone

    @staticmethod
    def getDroneData(drone: Drone) -> object:
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
            "distanceUp": drone.distanceUp,
            "distanceFront": drone.distanceFront,
            "distanceBack": drone.distanceBack,
            "distanceLeft": drone.distanceLeft,
            "distanceRight": drone.distanceRight,
            "ldr": drone.ldr,
            "colorFront": drone.colorFront,
            "colorBack": drone.colorBack
        }