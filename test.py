import random
import numpy as np
import math
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

class Drone:
    def __init__(self, droneId: str, master: bool, locationX: int, locationY: int):
        self.droneId = droneId
        self.master = master
        self.locationX = locationX
        self.locationY = locationY
        # self.locationX = random.randint(0, 1919) 
        # self.locationY = random.randint(0, 1079) 

class Swarm:
    def __init__(self):
        self.softwareDrones = []
        self.hardwareDrones = []
        self.drones = []
        self.masterDroneIsHardware = False
        self.masterDrone = None

    def addSoftwareDrone(self, drone: Drone) -> None:
        if drone.master:
            self.masterDrone = drone
            self.masterDroneIsHardware = False
        else:
            self.softwareDrones.append(drone)

    def addHardwareDrone(self, drone: Drone) -> None:
        if drone.master:
            self.masterDrone = drone
            self.masterDroneIsHardware = True
        else:
            self.hardwareDrones.append(drone)

    def calculateOptimalPlaces(self) -> object:
        self.drones = self.softwareDrones + self.hardwareDrones + [self.masterDrone]
        startingLocations = self.__getStartingLocations()
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
        elif numberOfHardwareDrones >= numberOfSoftwareDrones:
            if self.masterDroneIsHardware:
                masterDroneIndex = masterDroneIndex * 2
            else:
                masterDroneIndex = masterDroneIndex * 2 + 1

            droneOrder[masterDroneIndex] = self.masterDrone
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.hardwareDrones, masterDroneIndex, startingLocations, True)
            startingLocations = self.__getStartingLocations()
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.softwareDrones, masterDroneIndex, startingLocations, False, 1)
        elif numberOfHardwareDrones < numberOfSoftwareDrones:
            if not self.masterDroneIsHardware:
                masterDroneIndex = masterDroneIndex * 2
            else:
                masterDroneIndex = masterDroneIndex * 2 + 1

            droneOrder[masterDroneIndex] = self.masterDrone
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.softwareDrones, masterDroneIndex, startingLocations, False)
            startingLocations = self.__getStartingLocations()
            droneOrder = self.__calculateDroneOrderByMultipleKindsOfDrones(droneOrder, self.hardwareDrones, masterDroneIndex, startingLocations, True, 1)

        self.drones = []
        sortedDroneOrder = sorted(droneOrder.keys())
        for drone in sortedDroneOrder:
            self.drones.append(droneOrder[drone])

        return droneOrder

    # Calculate distance between drone and point
    @staticmethod
    def __calculateDistanceBetweenDroneAndPoint(drone: Drone, point: []) -> int:
        return math.sqrt(pow(drone.locationX - point[0], 2) + pow(drone.locationY - point[1], 2))

    # Get the starting coordinates for the drones
    def __getStartingLocations(self) -> []:
        startCoordinates = []
        for index, drone in enumerate(self.drones):
            locationX = 300
            locationY = 200 + (100 * index)
            startCoordinates.append([locationX, locationY])
        return startCoordinates

    # Calculate the order for one kind of drone
    def __calculateDroneOrderByOneKindOfDrone(self, droneOrder: {}, drones: [], masterDroneIndex: int, startingLocations = []) -> {}:
        droneLocations = []
        startingLocations.pop(masterDroneIndex)
        for drone in drones:
            droneLocations.append([drone.locationX, drone.locationY])

        costMatrix = cdist(droneLocations, startingLocations, "sqeuclidean")
        _, optionalLocation = linear_sum_assignment(costMatrix)
        
        for index in range(len(drones)):
            setIndex = index + 1 if index >= masterDroneIndex else index
            droneOrder[setIndex] = drones[optionalLocation[index]]
        
        return droneOrder

    # Calculate the order for multiple kinds of drones
    def __calculateDroneOrderByMultipleKindsOfDrones(self, droneOrder: {}, drones: [], masterDroneIndex: int, startingLocations = [], hardwareDrones: bool = False, positionAdder: int = 0) -> {}:
        droneLocations = []

        for drone in drones:
            droneLocations.append([drone.locationX, drone.locationY])

        newStartingLocations = []
        for locationIndex in range(len(startingLocations)):
            if masterDroneIndex == locationIndex:
                continue
            if positionAdder == 0 and locationIndex % 2 == 0:
                newStartingLocations.append(startingLocations[locationIndex])
            elif positionAdder == 1 and locationIndex % 2 == 1:
                newStartingLocations.append(startingLocations[locationIndex])

        costMatrix = cdist(droneLocations, newStartingLocations, "sqeuclidean")
        _, optionalLocation = linear_sum_assignment(costMatrix)

        for index in range(len(drones)):
            setIndex = index * 2 + positionAdder
            if self.masterDroneIsHardware == hardwareDrones:
                setIndex = setIndex + 2 if setIndex >= masterDroneIndex else setIndex
            droneOrder[setIndex] = drones[optionalLocation[index]]
        
        return droneOrder

def printDroneOrder(droneOrder):
    sortedDictionary = sorted(droneOrder.keys())
    for x in sortedDictionary:
        print(droneOrder[x].droneId, droneOrder[x].master)

if __name__ == '__main__':
    sDroneOne = Drone("S1", False, 0, 0)
    sDroneTwo = Drone("S2", False, 0, 0)
    sDroneThree = Drone("S3", False, 0, 0)
    hDroneOne = Drone("H1", True, 300, 300)
    hDroneTwo = Drone("H2", False, 300, 200)
    hDroneThree = Drone("H3", False, 300, 500)

    swarm = Swarm()
    swarm.addSoftwareDrone(sDroneOne)
    swarm.addSoftwareDrone(sDroneTwo)
    # swarm.addSoftwareDrone(sDroneThree)
    swarm.addHardwareDrone(hDroneOne)
    swarm.addHardwareDrone(hDroneTwo)
    swarm.addHardwareDrone(hDroneThree)

    droneOrder = swarm.calculateOptimalPlaces()
    printDroneOrder(droneOrder)