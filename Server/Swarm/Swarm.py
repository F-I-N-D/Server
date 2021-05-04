from Server.Drone.Drone import Drone

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

    # Hier moet de code komen om de drones in de swarm aan te sturen