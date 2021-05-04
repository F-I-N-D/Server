import socket
from threading import Thread
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone

class Socket(Thread):
    def __init__(self, port: int):
        Thread.__init__(self)
        self.__isRunnning = False
        self.softwareDrones = []
        self.hardwareDrones = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', port))

    def stop(self) -> None:
        self.__isRunnning = False
        self.socket.close()

    def addHardwareDrone(self, drone: HardwareDrone) -> None:
        self.hardwareDrones.append(drone)

    def addSoftwareDrone(self, drone: SoftwareDrone) -> None:
        self.softwareDrones.append(drone)

    def run(self):
        self.__isRunnning = True
        socket.listen(1)
        client, address = socket.accept()
        while True and self.__isRunnning:
            # Hier komt de socket code wanneer het protocol tussen
            # de simulatie en de server bekend is
            response = client.recv(255)
            if response != "":
                print(response)