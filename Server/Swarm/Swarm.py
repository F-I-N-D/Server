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
            drone.takeOff()

        time.sleep(2)

        for drone in self.drones:
            drone.up()
        
        time.sleep(2)

        for drone in self.drones:
            drone.stop()

        for drone in self.drones:
            drone.forward()

        time.sleep(4)

        for drone in self.drones:
            drone.stop()

        for drone in self.drones:
            drone.turnRight()

        time.sleep(5)

        for drone in self.drones:
            drone.stop()

        for drone in self.drones:
            drone.forward()

        time.sleep(4)

        for drone in self.drones:
            drone.stop()

        for drone in self.drones:
            drone.turnRight()

        time.sleep(5)

        for drone in self.drones:
            drone.stop()

        for drone in self.drones:
            drone.land()

        for drone in self.drones:
            drone.disconnect()

        time.sleep(1)
    # Hier moet de code komen om de drones in de swarm aan te sturen