import time
from threading import Thread
from Server.Drone.HardwareDrone import HardwareDrone

class GPS(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.__isRunnning = False
        self.drones = []

    def stop(self) -> None:
        self.__isRunnning = False

    def addDrone(self, drone: HardwareDrone) -> None:
        self.drones.append(drone)

    def run(self):
        self.__isRunnning = True
        while True and self.__isRunnning:
            time.sleep(10)
            # pass
            # Hier openCV code plaatsen
            # De drones zijn op te halen in de self.drones
            # Voorbeeld:
            # 
            # for drone in self.drones:
            #     if drone.color == color:
            #         drone.locationX = x
            #         drone.locationY = Y