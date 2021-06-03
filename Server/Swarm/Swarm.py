from Server.Drone.Drone import Drone
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone
import operator
import time
import enum
import math
from threading import Thread

DRONE_HEIGHT = 50
DRONE_DISTANCE = 75
BORDER_WIDTH_X = 300
BORDER_WIDTH_Y = 200
SCREEN_SIZE_X = 1920
SCREEN_SIZE_Y = 1080
MIN_OBSTACLE_DISTANCE = 30

class Goal(enum.Enum):
    Search = 0
    Scatter = 1
    Calibrate = 2

class Action(enum.Enum):
    Connect = 10
    Search = 20
    Calibrate = 21
    Scatter = 22
    Disconnect = 23
    Kill = 30

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

        self.drones = self.hardwareDrones + self.softwareDrones + [self.masterDrone]

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
                self.kill()
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
        print(self.drones)
        for drone in self.drones:
            if not drone.isConnected():
                return False

        return True

    def fly(self) -> None:
        for drone in self.drones:
            drone.takeOff(0.8)

        time.sleep(1)

        targetReached = True
        location = []
        itteration = 0

        if self.goal == Goal.Search or self.goal == Goal.Calibrate:
            location = self.getStartingLocations()
            targetReached = False
            for index, drone in enumerate(self.drones):
                drone.setTarget(location[index][0], location[index][1], DRONE_HEIGHT - 15 if drone.master else DRONE_HEIGHT)

        while self.goal != None:
            self.safetyCheck()
            if self.goal == Goal.Search and targetReached:
                pass
            elif self.goal == Goal.Calibrate and targetReached:
                location = self.getCalibrateLocations(itteration)
                if location == []:
                    self.goal = None
                    continue
                for index, drone in enumerate(self.drones):
                    drone.setTarget(location[index][0], location[index][1], DRONE_HEIGHT - 15 if drone.master else DRONE_HEIGHT)
                targetReached = False
                itteration += 1
            elif self.goal == Goal.Scatter and targetReached:
                pass

            if location == []:
                self.goal = None

            targetReached = True
            
            for drone in self.drones:
                drone.adjust()

                if not drone.targetReached:
                    targetReached = False

                if self.action == Action.Calibrate:
                    if drone.ldr > drone.ldrMax:
                        drone.ldrMax = drone.ldr

                # Dit herschrijven zodat de bounding box ook wordt aangepast? Of in ieder geval dat de drone niet gelijk de target haalt
                # maar dat hij eerst dan wel naar zijn Y gaat en X dan laat gaan bijvoorbeeld
                # if drone.master:
                #     if 0 < drone.distanceFront < MIN_OBSTACLE_DISTANCE or 0 < drone.distanceBack < MIN_OBSTACLE_DISTANCE or \
                #     0 < drone.distanceLeft < MIN_OBSTACLE_DISTANCE or 0 < drone.distanceRight < MIN_OBSTACLE_DISTANCE:
                #         targetReached = True

                for comparingDrone in self.drones:
                    if drone.droneId == comparingDrone.droneId:
                        continue

                    if 0 < self.calculateDistanceBetweenDrones(drone, comparingDrone) < 50:
                        print(self.calculateDistanceBetweenDrones(drone, comparingDrone))
                        # Hoeken 90 graden draaien naar buiten dan wel links recht licht aan de richting en de plaats van de drones

            if self.action == Action.Kill:
                self.goal = None

            time.sleep(0.05)

        time.sleep(1)
        self.land()

        if self.action == Action.Calibrate:
            f = open("ldrCalibrate.csv", "w")
            for drone in self.drones:
                f.write(f"{drone.droneId},{drone.ldrMax}\n")
            f.close

    @staticmethod
    def calculateDistanceBetweenDrones(droneOne: Drone, droneTwo: Drone) -> int:
        return math.sqrt(pow(droneOne.locationX - droneTwo.locationX, 2) + pow(droneOne.locationY - droneTwo.locationY, 2))

    def land(self):
        for drone in self.drones:
            drone.land()
            drone.disconnect()

    def disconnect(self):
        for drone in self.drones:
            drone.disconnect()

    def kill(self):
        for drone in self.drones:
            drone.kill()

    def getStartingLocations(self) -> []:
        startCoordinates = []
        for index, drone in enumerate(self.drones):
            xLocation = BORDER_WIDTH_X
            yLocation = BORDER_WIDTH_Y + (DRONE_DISTANCE * index)
            startCoordinates.append([xLocation, yLocation])
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

        if itteration == 0:
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, BORDER_WIDTH_Y])
            coordinates += startCoordinates
        else:
            if (itteration % 2) == 0:
                # shift swarm to right
                numDronesToSidesOfMaster = (numberOfDrones - 1) / 2

                xLocation = masterDrone.locationX
                newMasterY = masterDrone.locationY + numberOfDrones * DRONE_DISTANCE
                if newMasterY + ((numberOfDrones * DRONE_DISTANCE) / 2) > SCREEN_SIZE_Y - BORDER_WIDTH_Y:
                    for index, drone in enumerate(self.drones):
                        yLocation = (SCREEN_SIZE_Y - BORDER_WIDTH_Y) - DRONE_DISTANCE * index
                        coordinates.append([xLocation, yLocation])
                else:
                    for index in range(numDronesToSidesOfMaster):
                        yLocation = newMasterY - (DRONE_DISTANCE * (index + 1))
                        coordinates.append([xLocation, yLocation])
                    ylocation = newMasterY
                    coordinates.append([xLocation, yLocation])
                    for index in range(numDronesToSidesOfMaster):
                        yLocation = newMasterY + (DRONE_DISTANCE * (index + 1))
                        coordinates.append([xLocation, yLocation])
            else:
                #move swarm forwards or backwards
                if masterDrone.locationX < (BORDER_WIDTH_X + 100):
                    #swarm is on bottom side of searching location, move forwards
                    for index, drone in enumerate(self.drones):
                        xLocation = SCREEN_SIZE_X - BORDER_WIDTH_X
                        yLocation = drone.locationY
                        coordinates.append([xLocation, yLocation])

                elif if masterDrone.locationX > (BORDER_WIDTH_X - 100):
                    #swarm is on top side of searching location, move backwards
                    for index, drone in enumerate(self.drones):
                        xLocation = BORDER_WIDTH_X
                        yLocation = drone.locationY
                        coordinates.append([xLocation, yLocation])
        return coordinates
    
    def safetyCheck(self):
        numberOfDrones = len(self.drones)
        for drone in enumerate(self.drones):
            if drone.xLocation < (BORDER_WIDTH_X / 2) or drone.xLocation > (SCREEN_SIZE_X - (BORDER_WIDTH_X / 2)):
                #kill any drones getting too close to exiting the left and right of the frame
                drone.kill()
                print(f"Drone: {drone.droneId} tried to escape and has been terminated.")
            if drone.yLocation < (BORDER_WIDTH_Y / 2) or drone.yLocation > (SCREEN_SIZE_Y - (BORDER_WIDTH_Y / 2)):
                #kill any drones getting too close to exiting the top and bottom of the frame
                drone.kill()
                print(f"Drone: {drone.droneId} tried to escape and has been terminated.")
  