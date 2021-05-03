import logging
import time
import cflib.crtp
from .Swarm.Swarm import Swarm
from .Drone.HardwareDrone import HardwareDrone
from .Drone.SoftwareDrone import SoftwareDrone
from .Drone.TerminalDrone import TerminalDrone

uriMaster = 'radio://0/20/2M/E7E7E7E700'
uriOne = 'radio://0/20/2M/E7E7E7E701'
uriTwo = 'radio://0/20/2M/E7E7E7E702'

logging.basicConfig(level=logging.ERROR)

class Server:
    def __init__(self):
        cflib.crtp.init_drivers()
        self.swarm = Swarm()

    def start(self) -> None:
        masterDrone = TerminalDrone('one', 'white', True)
        self.swarm.addDrone(masterDrone)
        self.swarm.connect()
        self.swarm.isConnected()

#     droneMaster = HardwareDrone(uriOne, 'white')
#     droneMaster.connect()

#     # droneOne = HardwareDrone(uriOne)
#     # droneOne.connect()

#     # droneTwo = HardwareDrone(uriTwo)
#     # droneTwo.connect()
    
#     while not droneMaster.isConnected():
#         time.sleep(0.5)
#         print('Connecting...')

#     print('Connected')

#     # while not droneOne.isConnected():
#     #     time.sleep(0.1)

#     # while not droneTwo.isConnected():
#     #     time.sleep(0.1)

#     # droneOne.addLogger()

#     droneMaster.takeOff()
#     # droneOne.takeOff()
#     # droneTwo.takeOff()

#     # while values == {}:
#     #     time.sleep(0.1)

#     # if (values['pm.state'] == 1):
#     #     print('You can\'t fly while charging')
#     #     print(f'You are at {values["pm.batteryLevel"]}%')
#     #     os._exit(0)

#     # print(f'You are at {values["pm.batteryLevel"]}%')

#     time.sleep(1)
#     droneMaster.up()
#     # droneOne.up()
#     # droneTwo.up()
#     time.sleep(2)
#     droneMaster.stop()
#     # droneOne.stop()
#     # droneTwo.stop()
#     time.sleep(1)

#     # droneMaster.forward()
#     # droneOne.forward()
#     # droneTwo.forward()
#     # time.sleep(5)
#     # droneMaster.stop()
#     # droneOne.stop()
#     # droneTwo.stop()
#     time.sleep(1)

#     droneMaster.down()
#     # droneOne.down()
#     # droneTwo.down()
#     time.sleep(3)

#     os._exit(0)
