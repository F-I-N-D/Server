import operator
import time
import enum
import math
from threading import Thread
import numpy as np

from Server.Drone.Drone import Drone
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone
from Server.Swarm.Action import Action
from Server.Swarm.Goal import Goal

DRONE_HEIGHT = 50
MASTER_LOWER_HEIGHT = 15
DRONE_DISTANCE = 100
BORDER_WIDTH_X = 300
BORDER_WIDTH_Y = 200
SCREEN_SIZE_X = 1920
SCREEN_SIZE_Y = 1080
MIN_OBSTACLE_DISTANCE = 30
DEFAULT_CIRCLE_RADIUS = 100
MAX_AMOUNT_OF_FRAMES_NOT_SEEN = 10

class Swarm(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__isRunnning = False
        self.softwareDrones = []
        self.hardwareDrones = []
        self.drones = []
        self.masterDroneIsHardware = False
        self.masterDrone = None
        self.goal = None
        self.action = None
    
    def stop(self) -> None:
        self.__isRunnning = False

    def run(self):
        self.__isRunnning = True

        self.calculateOptimalPlaces()

        while self.__isRunnning:
            if self.action == Action.Connect:
                self.connect()
                self.action = None
            elif self.action == Action.Search:
                self.goal = Goal.Search
                self.fly()
                self.action = None
            elif self.action == Action.Calibrate:
                self.goal = Goal.Calibrate
                self.fly()
                self.action = None
            elif self.action == Action.Scatter:
                self.goal = Goal.Scatter
                self.fly()
                self.action = None
            elif self.action == Action.Disconnect:
                self.disconnect()
                self.action = None
            elif self.action == Action.Kill:
                self.action = None
            else:
                time.sleep(0.1)

    def calculateOptimalPlaces(self) -> None:
        numberOfHardwareDrones = len(self.hardwareDrones)
        numberOfSoftwareDrones = len(self.softwareDrones)
        numberOfDrones = numberOfHardwareDrones + numberOfSoftwareDrones + 1

        if self.masterDroneIsHardware:
            masterDroneIndex = int(numberOfHardwareDrones / 2)
            numberOfHardwareDrones += 1
        else:
            masterDroneIndex = int(numberOfSoftwareDrones / 2)
            numberOfSoftwareDrones += 1

        droneOrder = {}
        if numberOfHardwareDrones == numberOfSoftwareDrones:
            masterDroneSet = False
            for index, drone in enumerate(self.hardwareDrones):
                if masterDroneSet:
                    index += 1

                if index * 2 == masterDroneIndex * 2 and self.masterDroneIsHardware:
                    droneOrder[index * 2] = self.masterDrone
                    droneOrder[(index + 1) * 2] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index * 2] = drone

            masterDroneSet = False
            for index, drone in enumerate(self.softwareDrones):
                if masterDroneSet:
                    index += 1

                if index * 2 + 1 == masterDroneIndex * 2 + 1 and not self.masterDroneIsHardware:
                    droneOrder[index * 2 + 1] = self.masterDrone
                    droneOrder[(index + 1) * 2 + 1] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index * 2 + 1] = drone
        elif numberOfSoftwareDrones == 0:
            masterDroneSet = False
            for index, drone in enumerate(self.hardwareDrones):
                if masterDroneSet:
                    index += 1

                if index == masterDroneIndex and self.masterDroneIsHardware:
                    droneOrder[index] = self.masterDrone
                    droneOrder[index + 1] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index] = drone
        elif numberOfHardwareDrones == 0:
            masterDroneSet = False
            for index, drone in enumerate(self.softwareDrones):
                if masterDroneSet:
                    index += 1

                if index == masterDroneIndex and not self.masterDroneIsHardware:
                    droneOrder[index] = self.masterDrone
                    droneOrder[index + 1] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index] = drone
        elif numberOfHardwareDrones > numberOfSoftwareDrones:
            masterDroneSet = False
            for index, drone in enumerate(self.hardwareDrones):
                if masterDroneSet:
                    index += 1

                if index * 2 == masterDroneIndex * 2 and self.masterDroneIsHardware:
                    droneOrder[index * 2] = self.masterDrone
                    droneOrder[(index + 1) * 2] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index * 2] = drone

            masterDroneSet = False
            for index, drone in enumerate(self.softwareDrones):
                if masterDroneSet:
                    index += 1

                if index * 2 + 1 == masterDroneIndex * 2 + 1 and not self.masterDroneIsHardware:
                    droneOrder[index * 2 + 1] = self.masterDrone
                    droneOrder[(index + 1) * 2 + 1] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index * 2 + 1] = drone
        elif numberOfHardwareDrones < numberOfSoftwareDrones:
            masterDroneSet = False
            for index, drone in enumerate(self.softwareDrones):
                if masterDroneSet:
                    index += 1

                if index * 2 == masterDroneIndex * 2 and not self.masterDroneIsHardware:
                    droneOrder[index * 2] = self.masterDrone
                    droneOrder[(index + 1) * 2] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index * 2] = drone

            for index, drone in enumerate(self.hardwareDrones):
                if masterDroneSet:
                    index += 1

                if index * 2 + 1 == masterDroneIndex * 2 + 1 and self.masterDroneIsHardware:
                    droneOrder[index * 2 + 1] = self.masterDrone
                    droneOrder[(index + 1) * 2 + 1] = drone
                    masterDroneSet = True
                else:
                    droneOrder[index * 2 + 1] = drone

        sortedDroneOrder = sorted(droneOrder.keys())
        for drone in sortedDroneOrder:
            self.drones.append(droneOrder[drone])

    def addSoftwareDrone(self, drone: SoftwareDrone) -> None:
        if drone.master:
            self.masterDrone = drone
            self.masterDroneIsHardware = False
        else:
            self.softwareDrones.append(drone)

    def addHardwareDrone(self, drone: HardwareDrone) -> None:
        if drone.master:
            self.masterDrone = drone
            self.masterDroneIsHardware = True
        else:
            self.hardwareDrones.append(drone)

    def connect(self) -> None:
        for drone in self.drones:
            drone.connect()
        
    def isConnected(self) -> bool:
        for drone in self.drones:
            if not drone.isConnected():
                return False

        return True

    def fly(self) -> None:
        for drone in self.drones:
            drone.takeOff(DRONE_HEIGHT - MASTER_LOWER_HEIGHT if drone.master else DRONE_HEIGHT)

        time.sleep(1)

        targetReached = True
        location = []
        itteration = 0
        targetLocation = None

        if self.goal == Goal.Search or self.goal == Goal.Calibrate:
            location = self.getStartingLocations()
            targetReached = False
            for index, drone in enumerate(self.drones):
                drone.setTarget(location[index][0], location[index][1])

        if self.goal == Goal.Search:
            f = open("ldrCalibrate.csv", "r")
            data = f.readlines()
            for droneValue in data:
                for drone in self.drones:
                    splittedValue = droneValue.split(',')
                    if drone.droneId == splittedValue[0]:
                        drone.ldrMax = float(splittedValue[1])
                        
        while self.goal != None:
            self.safetyCheck()
            if self.goal == Goal.Search and targetReached:
                location = self.getSearchLocations(itteration)
                if location == []:
                    self.goal = None
                    continue
                for index, drone in enumerate(self.drones):
                    drone.setTarget(location[index][0], location[index][1])
                targetReached = False
                itteration += 1
            elif self.goal == Goal.Calibrate and targetReached:
                location = self.getCalibrateLocations(itteration)
                if location == []:
                    f = open("ldrCalibrate.csv", "w")
                    for drone in self.drones:
                        f.write(f"{drone.droneId},{drone.ldrMax}\n")
                    f.close
                    self.goal = None
                    continue
                for index, drone in enumerate(self.drones):
                    drone.setTarget(location[index][0], location[index][1])
                targetReached = False
                itteration += 1
            elif self.goal == Goal.Scatter and targetReached:
                pass
            elif self.goal == Goal.FollowTarget and targetReached:
                location = self.getCircleLocations(targetLocation[0], targetLocation[1])
                if location == []:
                    self.goal = None
                    continue
                for index, drone in enumerate(self.drones):
                    drone.setTarget(location[index][0], location[index][1], DRONE_HEIGHT - 15 if drone.master else DRONE_HEIGHT)
                targetReached = False
                itteration += 1

            targetReached = True
            
            for drone in self.drones:
                drone.adjust()

                if drone.framesNotSeen >= MAX_AMOUNT_OF_FRAMES_NOT_SEEN:
                    drone.kill("Drone is no longer seen by the GPS")

                if not drone.isConnected():
                    self.drones.remove(drone)
                    continue

                if not drone.targetReached:
                    targetReached = False

                if self.goal == Goal.Calibrate:
                    if drone.ldr > drone.ldrMax:
                        drone.ldrMax = drone.ldr

                if self.goal == Goal.Search:
                    if drone.ldr > drone.ldrMax * 1.2 and drone.ldrMax != 0:
                        self.goal = Goal.FollowTarget
                        targetReached = True
                        targetLocation = [drone.locationX, drone.locationY]

                # Dit herschrijven zodat de bounding box ook wordt aangepast? Of in ieder geval dat de drone niet gelijk de target haalt
                # maar dat hij eerst dan wel naar zijn Y gaat en X dan laat gaan bijvoorbeeld
                # if drone.master:
                #     if 0 < drone.distanceFront < MIN_OBSTACLE_DISTANCE or 0 < drone.distanceBack < MIN_OBSTACLE_DISTANCE or \
                #     0 < drone.distanceLeft < MIN_OBSTACLE_DISTANCE or 0 < drone.distanceRight < MIN_OBSTACLE_DISTANCE:
                #         targetReached = True

                # for comparingDrone in self.drones:
                #     if drone.droneId == comparingDrone.droneId:
                #         continue

                #     if 0 < self.calculateDistanceBetweenDrones(drone, comparingDrone) < 50:
                #         print(self.calculateDistanceBetweenDrones(drone, comparingDrone))
                #         # Hoeken 90 graden draaien naar buiten dan wel links recht licht aan de richting en de plaats van de drones

            if self.action == Action.Kill:
                self.goal = None

            time.sleep(0.05)

        self.land()

    @staticmethod
    def calculateDistanceBetweenDrones(droneOne: Drone, droneTwo: Drone) -> int:
        return math.sqrt(pow(droneOne.locationX - droneTwo.locationX, 2) + pow(droneOne.locationY - droneTwo.locationY, 2))

    def land(self):
        for drone in self.drones:
            drone.land()

    def disconnect(self):
        for drone in self.drones:
            drone.disconnect()
            
    def kill(self):
        for drone in self.drones:
            drone.kill("Manual")

    def getStartingLocations(self) -> []:
        startCoordinates = []
        for index, drone in enumerate(self.drones):
            locationX = BORDER_WIDTH_X
            locationY = BORDER_WIDTH_Y + (DRONE_DISTANCE * index)
            startCoordinates.append([locationX, locationY])
        return startCoordinates

    def getCalibrateLocations(self, itteration) -> []:
        numberOfDrones = len(self.drones)
        startCoordinates = self.getStartingLocations()
        coordinates = []

        if itteration == 0:
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, BORDER_WIDTH_Y])
            coordinates += startCoordinates
        elif itteration == 1:
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, SCREEN_SIZE_Y - BORDER_WIDTH_Y])
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, BORDER_WIDTH_Y])
            coordinates += startCoordinates
        elif itteration == 2:
            coordinates.append([BORDER_WIDTH_X, SCREEN_SIZE_Y - BORDER_WIDTH_Y])
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, SCREEN_SIZE_Y - BORDER_WIDTH_Y])
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, BORDER_WIDTH_Y])
            coordinates += startCoordinates
        elif itteration >= 3:
            if itteration > 2 + numberOfDrones:
                return []

            coordinates += startCoordinates[::-1][0:itteration-2][::-1]
            coordinates.append([BORDER_WIDTH_X, SCREEN_SIZE_Y - BORDER_WIDTH_Y])
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, SCREEN_SIZE_Y - BORDER_WIDTH_Y])
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, BORDER_WIDTH_Y])
            coordinates += startCoordinates

        return coordinates

    def getSearchLocations(self, itteration) -> []:
        numberOfDrones = len(self.drones)
        startCoordinates = self.getStartingLocations()
        coordinates = []
        step = itteration % 2

        if self.drones[-1].locationY >= SCREEN_SIZE_Y - BORDER_WIDTH_Y - 50 and step == 1:
            print("hi")
            return []

        if step == 1:
            # shift swarm to right
            numDronesToSidesOfMaster = int((numberOfDrones - 1) / 2)

            locationX = self.masterDrone.locationX
            newMasterY = self.masterDrone.locationY + numberOfDrones * DRONE_DISTANCE
            if newMasterY + ((numberOfDrones * DRONE_DISTANCE) / 2) > SCREEN_SIZE_Y - BORDER_WIDTH_Y:
                for index, drone in enumerate(self.drones):
                    locationY = (SCREEN_SIZE_Y - BORDER_WIDTH_Y) - DRONE_DISTANCE * index
                    coordinates.append([locationX, locationY])
                coordinates = coordinates[::-1]
            else:
                for index in range(numDronesToSidesOfMaster):
                    locationY = newMasterY - (DRONE_DISTANCE * (index + 1))
                    coordinates.append([locationX, locationY])
                locationY = newMasterY
                coordinates.append([locationX, locationY])
                for index in range(numDronesToSidesOfMaster):
                    locationY = newMasterY + (DRONE_DISTANCE * (index + 1))
                    coordinates.append([locationX, locationY])
        else:
            #move swarm forwards or backwards
            if self.masterDrone.locationX < (BORDER_WIDTH_X + 100):
                #swarm is on bottom side of searching location, move forwards
                for index, drone in enumerate(self.drones):
                    locationX = SCREEN_SIZE_X - BORDER_WIDTH_X
                    locationY = drone.locationY
                    coordinates.append([locationX, locationY])

            elif self.masterDrone.locationX > (BORDER_WIDTH_X - 100):
                #swarm is on top side of searching location, move backwards
                for index, drone in enumerate(self.drones):
                    locationX = BORDER_WIDTH_X
                    locationY = drone.locationY
                    coordinates.append([locationX, locationY])
        return coordinates

    def getCircleLocations(self, locationX, locationY) -> []:
        numberOfDrones = len(self.drones)
        vector = np.array([DEFAULT_CIRCLE_RADIUS, 0])
        centerPoint = np.array([locationX, locationY])
        degreesPerDrone = 360 / numberOfDrones

        resultArray = []
        for droneItterator in range(numberOfDrones):
            if droneItterator == numberOfDrones:
                break
            currentRotation = np.radians(degreesPerDrone * droneItterator)
            rotationMatrix = np.array([[math.cos(currentRotation), -1 * math.sin(currentRotation)], [math.sin(currentRotation), math.cos(currentRotation)]])
            result = np.add(np.matmul(rotationMatrix, vector), centerPoint)
            resultArray.append(result.tolist())

        return resultArray

    def safetyCheck(self):
        numberOfDrones = len(self.drones)
        for drone in self.drones:
            if drone.locationX < (BORDER_WIDTH_X / 2) or drone.locationX > (SCREEN_SIZE_X - (BORDER_WIDTH_X / 2)):
                #kill any drones getting too close to exiting the left and right of the frame
                drone.kill("Tried to escape")
            if drone.locationY < (BORDER_WIDTH_Y / 2) or drone.locationY > (SCREEN_SIZE_Y - (BORDER_WIDTH_Y / 2)):
                #kill any drones getting too close to exiting the top and bottom of the frame
                drone.kill("Tried to escape")