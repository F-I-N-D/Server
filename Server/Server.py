import logging
import time
import cflib.crtp
from Server.Swarm.Swarm import Swarm
from Server.GPS.GPS import GPS
from Server.Socket.Socket import Socket
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone
from Server.Logger.Logger import Logger

idMaster = 'E7E7E7E700'
idOne = 'E7E7E7E701'
idTwo = 'E7E7E7E702'
idThree = '3'
idFour = '4'

logging.basicConfig(level=logging.ERROR)

class Server:
    def __init__(self):
        self.swarm = Swarm()
        self.gps = GPS()
        self.socket = Socket(8000)
        self.logger = Logger()

    def start(self) -> None:
        self.logger.info("Start")
        cflib.crtp.init_drivers()

        # droneMaster = HardwareDrone(idMaster, self.logger, 'white', True)
        # self.swarm.addDrone(droneMaster)
        # self.gps.addDrone(droneMaster)
        # self.socket.addHardwareDrone(droneMaster)

        droneOne = HardwareDrone(idOne, self.logger, 'green', 'blue')
        self.swarm.addDrone(droneOne)
        self.gps.addDrone(droneOne)
        self.socket.addHardwareDrone(droneOne)

        droneTwo = HardwareDrone(idTwo, self.logger, 'red', 'blue')
        self.swarm.addDrone(droneTwo)
        self.gps.addDrone(droneTwo)
        self.socket.addHardwareDrone(droneTwo)

        # droneThree = SoftwareDrone(idThree, self.logger, 'green', 'yellow')
        # self.swarm.addDrone(droneThree)
        # self.socket.addSoftwareDrone(droneThree)

        # droneFour = SoftwareDrone(idFour, self.logger, 'blue', 'yellow')
        # self.swarm.addDrone(droneFour)
        # self.socket.addSoftwareDrone(droneFour)

        self.gps.start()
        self.socket.start()

        self.swarm.connect()

        while not self.swarm.isConnected():
            print('Connecting')
            time.sleep(1)

        print('Connected')

        time.sleep(0.1)

        # droneMaster.logData()
        droneOne.logData()
        droneTwo.logData()
        # droneThree.logData()

        # self.swarm.search()

        while True:
            time.sleep(10)

        # droneMaster.logData()
        droneOne.logData()
        droneTwo.logData()
        # droneThree.logData()

        self.logger.info("End")

        self.gps.stop()
        self.socket.stop()