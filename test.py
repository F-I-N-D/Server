import random

class Drone:
    def __init__(self, droneId: str, master: bool):
        self.droneId = droneId
        self.master = master
        self.locationX = random.randint(0, 1919) 
        self.locationY = random.randint(0, 1079) 

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

        return droneOrder

def printDroneOrder(droneOrder):
    sortedDictionary = sorted(droneOrder.keys())
    for x in sortedDictionary:
        print(droneOrder[x].droneId, droneOrder[x].master)

if __name__ == '__main__':
    sDroneOne = Drone("S1", True)
    sDroneTwo = Drone("S2", False)
    sDroneThree = Drone("S3", False)
    hDroneOne = Drone("H1", True)
    hDroneTwo = Drone("H2", False)
    hDroneThree = Drone("H3", False)

    swarm = Swarm()
    swarm.addSoftwareDrone(sDroneOne)
    swarm.addSoftwareDrone(sDroneTwo)
    swarm.addSoftwareDrone(sDroneThree)
    # swarm.addHardwareDrone(hDroneOne)
    # swarm.addHardwareDrone(hDroneTwo)
    # swarm.addHardwareDrone(hDroneThree)

    droneOrder = swarm.calculateOptimalPlaces()
    printDroneOrder(droneOrder)
    