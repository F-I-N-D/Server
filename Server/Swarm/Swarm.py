import operator
import time
import math
import random
from threading import Thread
import numpy as np

from Server.Drone.Drone import Drone
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone
from Server.Swarm.Action import Action
from Server.Swarm.Goal import Goal
from Server.Logger.Logger import Logger

# Constants
DRONE_HEIGHT = 80
MASTER_LOWER_HEIGHT = 0
DRONE_DISTANCE = 100
BORDER_WIDTH_X = 300
BORDER_WIDTH_Y = 200
SCREEN_SIZE_X = 1920
SCREEN_SIZE_Y = 1080
MIN_OBSTACLE_DISTANCE = 30
DEFAULT_CIRCLE_RADIUS = 100
MAX_AMOUNT_OF_FRAMES_NOT_SEEN = 10
CALIBRATION_FILE = "ldrCalibrate.csv"

class Swarm(Thread):
    def __init__(self, logger: Logger):
        Thread.__init__(self)
        self.__isRunnning = False
        self.softwareDrones = []
        self.hardwareDrones = []
        self.drones = []
        self.masterDroneIsHardware = False
        self.masterDrone = None
        self.goal = Goal.Null
        self.action = Action.Null
        self.logger = logger
    
    # Stop the thread from running
    def stop(self) -> None:
        self.__isRunnning = False

    # Start the thread
    def run(self):
        self.__isRunnning = True

        # Calcualte best places for all droens
        self.calculateOptimalPlaces()

        while self.__isRunnning:
            # Preform action based on GUI option
            if self.action == Action.Connect:
                self.logger.info("Connecting to all drones")
                self.calculateOptimalPlaces()
                self.connect()
                self.action = Action.Null
            elif self.action == Action.Search:
                self.logger.info("Starting search")
                self.goal = Goal.Search
                self.fly()
                self.action = Action.Null
                self.logger.info("Search done")
            elif self.action == Action.Calibrate:
                self.logger.info("Starting calibrate")
                self.goal = Goal.Calibrate
                self.fly()
                self.action = Action.Null
                self.logger.info("Calibrate done")
            elif self.action == Action.Scatter:
                self.logger.info("Starting scatter")
                self.goal = Goal.Scatter
                self.fly()
                self.action = Action.Null
                self.logger.info("Scatter done")
            elif self.action == Action.Disconnect:
                self.logger.info("Disconnecting to all drones")
                self.disconnect()
                self.action = Action.Null
            else:
                time.sleep(0.1)

    # Add a software drone to the swam
    def addSoftwareDrone(self, drone: SoftwareDrone) -> None:
        if drone.master:
            self.masterDrone = drone
            self.masterDroneIsHardware = False
        else:
            self.softwareDrones.append(drone)

    # Add hardware drone to the swam
    def addHardwareDrone(self, drone: HardwareDrone) -> None:
        if drone.master:
            self.masterDrone = drone
            self.masterDroneIsHardware = True
        else:
            self.hardwareDrones.append(drone)

    # Connect all drones
    def connect(self) -> None:
        for drone in self.drones:
            drone.connect()
    
    # Check if all drones are connected
    def isConnected(self) -> bool:
        for drone in self.drones:
            if not drone.isConnected():
                return False

        self.logger.info("All drones connected")
        return True

    # Start flying
    def fly(self) -> None:
        # Make all drones take off
        for drone in self.drones:
            drone.takeOff(DRONE_HEIGHT - MASTER_LOWER_HEIGHT if drone.master else DRONE_HEIGHT)

        targetReached = True
        location = []
        itteration = 0
        targetLocation = None

        # Go to the starting position if the goal is search or calibrate
        if self.goal == Goal.Search or self.goal == Goal.Calibrate:
            location = self.getStartingLocations()
            targetReached = False
            for index, drone in enumerate(self.drones):
                drone.setTarget(location[index][0], location[index][1])

        # Load the calibrate data if the goal is search
        if self.goal == Goal.Search:
            f = open(CALIBRATION_FILE, "r")
            data = f.readlines()
            for droneValue in data:
                for drone in self.drones:
                    splittedValue = droneValue.split(',')
                    if drone.droneId == splittedValue[0]:
                        drone.ldrMax = float(splittedValue[1])
        
        # Run while a goal needs to be reached
        while self.goal != Goal.Null:
            # If target reached get the next location
            if self.goal == Goal.Search and targetReached:
                location = self.getSearchLocations(itteration)
            elif self.goal == Goal.Calibrate and targetReached:
                location = self.getCalibrateLocations(itteration)
            elif self.goal == Goal.Scatter and targetReached:
                location = self.getScatterLocations(itteration)
            elif self.goal == Goal.FollowTarget and targetReached:
                location = self.getCircleLocations(targetLocation[0], targetLocation[1])

            if targetReached:       
                # if there are no new locations save the calibrate data if the drones are calibrating
                # then set the goal to Null
                if location == []:
                    if self.goal == Goal.Calibrate:
                        f = open("ldrCalibrate.csv", "w")
                        for drone in self.drones:
                            f.write(f"{drone.droneId},{drone.ldrMax}\n")
                        f.close
                    self.goal = Goal.Null
                    continue
                # Assign a new target to each drone
                for index, drone in enumerate(self.drones):
                    drone.setTarget(location[index][0], location[index][1])
                itteration += 1

            targetReached = True
            
            # Check and adjust the speed fo all drones one for one
            for drone in self.drones:
                # Adjust the speed
                adjustmentVariables = self.collisionAdjust(drone)
                drone.adjust(adjustmentVariables[0], adjustmentVariables[1])

                # If the drone is no longer seen by the camera then it will be killed
                if drone.framesNotSeen >= MAX_AMOUNT_OF_FRAMES_NOT_SEEN:
                    drone.kill("Drone is no longer seen by the GPS")
                    self.removeDroneFromList(drone)
                    continue

                # If the drone trys to excape from the area it will be killed
                if drone.locationX < (BORDER_WIDTH_X / 4) or drone.locationX > (SCREEN_SIZE_X - (BORDER_WIDTH_X / 4)):
                    drone.kill("Tried to escape on x")
                    self.removeDroneFromList(drone)
                    continue
                
                if drone.locationY < (BORDER_WIDTH_Y / 4) or drone.locationY > (SCREEN_SIZE_Y - (BORDER_WIDTH_Y / 4)):
                    drone.kill("Tried to escape on y")
                    self.removeDroneFromList(drone)
                    continue

                # If the drone is no longer connected it will be removed
                if not drone.isConnected():
                    self.removeDroneFromList(drone)
                    continue

                if not drone.targetReached and drone.isFlying:
                    targetReached = False

                # Save highest LDR data if callibrating
                if self.goal == Goal.Calibrate:
                    if drone.ldr > drone.ldrMax:
                        drone.ldrMax = drone.ldr

                # If goal is search check if the target is found
                if self.goal == Goal.Search:
                    if drone.ldr > drone.ldrMax * 1.1 and drone.ldrMax != 0:
                        self.goal = Goal.FollowTarget
                        targetReached = True
                        targetLocation = [drone.locationX, drone.locationY]

                # The master drone will check if the swarm is almost bumping into something
                if drone.master:
                    if (0 < drone.distanceFront < MIN_OBSTACLE_DISTANCE and drone.locationX < drone.targetLocationX) or \
                        (0 < drone.distanceBack < MIN_OBSTACLE_DISTANCE and drone.locationX > drone.targetLocationX):
                        for drone in self.drones:
                            drone.setTarget(drone.locationX, drone.targetLocationY)

            if self.action == Action.Land:
                self.logger.info("Landing all drones")
                self.goal = Goal.Null

            if self.action == Action.Kill:
                self.logger.info("Killing all drones")
                self.goal = Goal.Null
                self.kill()

            time.sleep(0.05)

        self.land()

    # Calculate distance between drones
    @staticmethod
    def calculateDistanceBetweenDrones(droneOne: Drone, droneTwo: Drone) -> int:
        return math.sqrt(pow(droneOne.locationX - droneTwo.locationX, 2) + pow(droneOne.locationY - droneTwo.locationY, 2))

    # Calculate distance between drone and point
    @staticmethod
    def calculateDistanceBetweenDroneAndPoint(drone: Drone, point: []) -> int:
        return math.sqrt(pow(drone.locationX - point[0], 2) + pow(drone.locationY - point[1], 2))

    # Land all drones
    def land(self):
        for drone in self.drones:
            drone.land()

    # Disconnect and remove all drones
    def disconnect(self):
        for drone in self.drones:
            drone.disconnect()
            self.removeDroneFromList(drone)
            
    # Kill and remove all drones
    def kill(self):
        for drone in self.drones:
            drone.kill("Manual")
            self.removeDroneFromList(drone)

    # Remove drone from the drone list
    def removeDroneFromList(self, droneToRemove: Drone):
        self.drones = [drone for drone in self.drones if drone.droneId != droneToRemove.droneId]

    # Get the starting coordinates for the drones
    def getStartingLocations(self) -> []:
        startCoordinates = []
        for index, drone in enumerate(self.drones):
            locationX = BORDER_WIDTH_X
            locationY = BORDER_WIDTH_Y + (DRONE_DISTANCE * index)
            startCoordinates.append([locationX, locationY])
        return startCoordinates

    # Get the next calibration locations for the drones
    def getCalibrateLocations(self, itteration: int) -> []:
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
            if itteration > numberOfDrones + 3:
                return []

            nextDronePlace = max(numberOfDrones - itteration, 0)
            coordinates += startCoordinates[nextDronePlace:nextDronePlace + itteration - 3]
            coordinates.append([BORDER_WIDTH_X, SCREEN_SIZE_Y - BORDER_WIDTH_Y])
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, SCREEN_SIZE_Y - BORDER_WIDTH_Y])
            coordinates.append([SCREEN_SIZE_X - BORDER_WIDTH_X, BORDER_WIDTH_Y])
            coordinates += startCoordinates

        return coordinates

    # Get the next search locations for the drones
    def getSearchLocations(self, itteration: int) -> []:
        numberOfDrones = len(self.drones)
        startCoordinates = self.getStartingLocations()
        coordinates = []
        step = itteration % 2

        if self.drones[-1].locationY >= SCREEN_SIZE_Y - BORDER_WIDTH_Y - 50 and step == 1:
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

    # Get the next circle locations for the drones
    def getCircleLocations(self, locationX: int, locationY: int) -> []:
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

    # Get the scatter locations for the drones
    def getScatterLocations(self, itteration: int) -> []:
        if itteration > 0:
            return []

        scatterLocations = []

        for drone in self.drones:
            locationX = random.randint(BORDER_WIDTH_X, SCREEN_SIZE_X - BORDER_WIDTH_X)
            locationY = random.randint(BORDER_WIDTH_Y, SCREEN_SIZE_Y - BORDER_WIDTH_Y)
            scatterLocations.append([locationX, locationY])
        return scatterLocations
        
    # If the drones almost collide move them around each other
    def collisionAdjust(self, drone1: Drone) -> []:
        collisionDistance = 0
        adjustmentVariables = [0, 0]
        for drone2 in self.drones:
            collisionDistance = self.calculateDistanceBetweenDrones(drone1, drone2)
            if(collisionDistance < 100):
                if((drone1.locationX - drone2.locationX) < 0):
                    #move to back
                    adjustmentVariables[0] = -1 * (1.1487 ** (abs(drone1.locationX - drone2.locationX)) - 1) / 10
                if((drone1.locationX - drone2.locationX) > 0):
                    #move to front
                    adjustmentVariables[0] = (1.1487 ** (abs(drone1.locationX - drone2.locationX)) - 1)  / 10
                if((drone1.locationY - drone2.locationY) < 0): 
                    #move to left
                    adjustmentVariables[1] = -1 * (1.1487 ** (abs(drone1.locationX - drone2.locationX)) - 1)  / 10
                if((drone1.locationY - drone2.locationY) > 0): 
                    #move to right
                    adjustmentVariables[1] = (1.1487 ** (abs(drone1.locationX - drone2.locationX)) - 1)  / 10

        adjustmentVariables[0] = max(min(0.5, adjustmentVariables[0]), -0.5)
        adjustmentVariables[1] = max(min(0.5, adjustmentVariables[1]), -0.5)
        adjustmentVariables = [0, 0]
        return adjustmentVariables

    # Calculate the optimal place for the drones so they have to travel as little as possible on startup
    def calculateOptimalPlaces(self) -> None:
        self.drones = self.softwareDrones + self.hardwareDrones + [self.masterDrone]
        startingLocations = self.getStartingLocations()
        softwareDrones = self.softwareDrones
        hardwareDrones = self.hardwareDrones

        if not self.masterDrone:
            raise ValueError("No master drone set")
            return

        numberOfHardwareDrones = len(hardwareDrones)
        numberOfSoftwareDrones = len(softwareDrones)
        numberOfDrones = numberOfHardwareDrones + numberOfSoftwareDrones + 1

        if self.masterDroneIsHardware:
            masterDroneIndex = int(numberOfHardwareDrones / 2)
            numberOfHardwareDrones += 1
        else:
            masterDroneIndex = int(numberOfSoftwareDrones / 2)
            numberOfSoftwareDrones += 1

        if (numberOfHardwareDrones - numberOfSoftwareDrones >= 2 or numberOfHardwareDrones - numberOfSoftwareDrones <= -2) \
            and numberOfHardwareDrones != 0 and numberOfSoftwareDrones != 0:
            raise ValueError("This swarm is not valid")
            return

        droneOrder = {}

        if numberOfSoftwareDrones == 0:
            droneOrder[masterDroneIndex] = self.masterDrone
            droneOrder = self.__calculateDroneOrderByOneKindOfDrone(droneOrder, self.hardwareDrones, masterDroneIndex, startingLocations)
        elif numberOfHardwareDrones == 0:
            droneOrder[masterDroneIndex] = self.masterDrone
            droneOrder = self.__calculateDroneOrderByOneKindOfDrone(droneOrder, self.softwareDrones, masterDroneIndex, startingLocations)
        elif numberOfHardwareDrones == numberOfSoftwareDrones or numberOfHardwareDrones > numberOfSoftwareDrones:
            if self.masterDroneIsHardware:
                masterDroneIndex = masterDroneIndex * 2
            else:
                masterDroneIndex = masterDroneIndex * 2 + 1

            droneOrder[masterDroneIndex] = self.masterDrone
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.hardwareDrones, masterDroneIndex, startingLocations, True)
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.softwareDrones, masterDroneIndex, startingLocations, False, 1)
        elif numberOfHardwareDrones < numberOfSoftwareDrones:
            if not self.masterDroneIsHardware:
                masterDroneIndex = masterDroneIndex * 2
            else:
                masterDroneIndex = masterDroneIndex * 2 + 1

            droneOrder[masterDroneIndex] = self.masterDrone
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.softwareDrones, masterDroneIndex, startingLocations, False)
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.hardwareDrones, masterDroneIndex, startingLocations, True, 1)

        self.drones = []
        sortedDroneOrder = sorted(droneOrder.keys())
        for drone in sortedDroneOrder:
            self.drones.append(droneOrder[drone])
    
    # Calculate the order for one kind of drone
    def __calculateDroneOrderByOneKindOfDrone(self, droneOrder: {}, drones: [], masterDroneIndex: int, startingLocations = []) -> {}:
        for index in range(len(drones)):
            index = index + 1 if index >= masterDroneIndex else index
            point = startingLocations[index]
            shortestDistance = 0
            closestDrone = None

            for drone in drones:
                distance = self.calculateDistanceBetweenDroneAndPoint(drone, point)
                if shortestDistance < distance or shortestDistance == 0:
                    shortestDistance = distance
                    closestDrone = drone

            droneOrder[index] = closestDrone
            drones = [drone for drone in drones if drone.droneId != closestDrone.droneId]
        return droneOrder

    # Calculate the order for multiple kinds of drones
    def __calculateDroneOrderByMultipleKindsOfDrones(self, droneOrder: {}, drones: [], masterDroneIndex: int, startingLocations = [], hardwareDrones: bool = False, positionAdder: int = 0) -> {}:
        for index in range(len(drones)):
            index = index * 2 + positionAdder
            if self.masterDroneIsHardware == hardwareDrones:
                index = index + 2 if index >= masterDroneIndex else index
            point = startingLocations[index]
            shortestDistance = 0
            closestDrone = None

            for drone in drones:
                distance = self.calculateDistanceBetweenDroneAndPoint(drone, point)
                if shortestDistance < distance or shortestDistance == 0:
                    shortestDistance = distance
                    closestDrone = drone

            droneOrder[index] = closestDrone
            drones = [drone for drone in drones if drone.droneId != closestDrone.droneId]
        return droneOrder