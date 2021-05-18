import logging
import time
import cflib.crtp
from Server.Swarm.Swarm import Swarm
from Server.GPS.GPS import GPS
from Server.Socket.Socket import Socket
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone
from Server.Drone.TerminalDrone import TerminalDrone

idMaster = 'E7E7E7E700'
idOne = 'E7E7E7E701'
idTwo = 'E7E7E7E702'
idThree = '3'

logging.basicConfig(level=logging.ERROR)

class Server:
    def __init__(self):
        self.swarm = Swarm()
        self.gps = GPS()
        self.socket = Socket(8000)

    def start(self) -> None:
        cflib.crtp.init_drivers()

        droneMaster = HardwareDrone(idMaster, 'white', True)
        self.swarm.addDrone(droneMaster)
        self.gps.addDrone(droneMaster)
        self.socket.addHardwareDrone(droneMaster)

        # droneTwo = HardwareDrone(idTwo, 'red')
        # self.swarm.addDrone(droneTwo)
        # self.gps.addDrone(droneTwo)
        # self.socket.addHardwareDrone(droneTwo)

        # droneThree = TerminalDrone(idThree, 'cyan')
        # self.swarm.addDrone(droneThree)
        
        self.gps.start()
        # self.socket.start()

        self.swarm.connect()

        while not self.swarm.isConnected():
            print('Connecting')
            time.sleep(0.5)
        
        droneMaster.addLogger()

        print('Connected')

        # self.swarm.search()

        self.gps.stop()