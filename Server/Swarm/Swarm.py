from Server.Drone.Drone import Drone
import operator
import time

class Swarm:
    def __init__(self):
        self.drones = []

    def addDrone(self, drone: Drone) -> None:
        self.drones.append(drone)

    def connect(self) -> None:
        for drone in self.drones:
            drone.connect()

    def isConnected(self) -> bool:
        for drone in self.drones:
            if not drone.isConnected():
                return False

        return True

    def search(self) -> None:
        for drone in self.drones:
            drone.takeOff(0.5)

        time.sleep(1)

        targetFound = False
        targetFound = self.goToLocation(300, 300)
        if targetFound:
            self.land()
            return

        targetFound = self.goToLocation(1620, 300)
        if targetFound:
            self.land()
            return

        targetFound = self.goToLocation(1620, 780)
        if targetFound:
            self.land()
            return

        targetFound = self.goToLocation(300, 780)
        if targetFound:
            self.land()
            return

        targetFound = self.goToLocation(300, 300)
        if targetFound:
            self.land()
            return

        time.sleep(1)

        self.land()

    def land(self):
        for drone in self.drones:
            drone.land()
            drone.disconnect()

    def goToLocation(self, newLocationX: int, newLocationY: int) -> bool:
        locationAchieved = False
        targetFound = False

        while not locationAchieved and not targetFound:
            for drone in self.drones:
                drone.adjust(newLocationX, newLocationY, 40)

                if drone.ldr > 1.3:
                    targetFound = True

                if drone.locationX > newLocationX - 25 and drone.locationX < newLocationX + 25 and drone.locationY > newLocationY - 25 and drone.locationY < newLocationY + 25:
                    locationAchieved = True
            
            time.sleep(0.1)

        return targetFound
