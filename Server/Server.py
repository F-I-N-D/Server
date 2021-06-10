import logging
import time
import cflib.crtp
from pynput import keyboard
from Server.Swarm.Swarm import Swarm, Action
from Server.GPS.GPS import GPS
from Server.Socket.Socket import Socket
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone
from Server.Logger.Logger import Logger
from Server.Logger.Level import Level
from Server.Gui.Gui import Gui, State
from rich.live import Live

idMaster = 'E7E7E7E700'
idOne = 'E7E7E7E701'
idTwo = 'E7E7E7E702'
idThree = '3'
idFour = '4'
idFive = '5'

logging.basicConfig(level=logging.ERROR)

class Server:
    def __init__(self):
        self.gui = Gui()
        self.swarm = Swarm()
        self.gps = GPS()
        self.socket = Socket(8000)
        self.logger = Logger(Level.Info)
        self.listener = keyboard.Listener(on_press = self.on_press)
        self.key = None

    def start(self) -> None:
        self.logger.info("Start")
        cflib.crtp.init_drivers()
        self.listener.start()

        # droneMaster = HardwareDrone(idMaster, self.logger, 'red', 'green', True)
        # self.swarm.addHardwareDrone(droneMaster)
        # self.gps.addDrone(droneMaster)
        # self.socket.addHardwareDrone(droneMaster)

        # droneOne = HardwareDrone(idOne, self.logger, 'green', 'blue')
        # self.swarm.addHardwareDrone(droneOne)
        # self.gps.addDrone(droneOne)
        # self.socket.addHardwareDrone(droneOne)

        # droneTwo = HardwareDrone(idTwo, self.logger, 'red', 'blue')
        # self.swarm.addHardwareDrone(droneTwo)
        # self.gps.addDrone(droneTwo)
        # self.socket.addHardwareDrone(droneTwo)

        droneThree = SoftwareDrone(idThree, self.logger, 'green', 'yellow')
        self.swarm.addSoftwareDrone(droneThree)
        self.socket.addSoftwareDrone(droneThree)

        droneFour = SoftwareDrone(idFour, self.logger, 'blue', 'yellow')
        self.swarm.addSoftwareDrone(droneFour)
        self.socket.addSoftwareDrone(droneFour)

        droneFive = SoftwareDrone(idFive, self.logger, 'red', 'yellow')
        self.swarm.addSoftwareDrone(droneFive)
        self.socket.addSoftwareDrone(droneFive)

        droneSix = SoftwareDrone('6', self.logger, 'blue', 'yellow', True)
        self.swarm.addSoftwareDrone(droneSix)
        self.socket.addSoftwareDrone(droneSix)

        droneSeven = SoftwareDrone('7', self.logger, 'blue', 'yellow')
        self.swarm.addSoftwareDrone(droneSeven)
        self.socket.addSoftwareDrone(droneSeven)

        # droneEight = SoftwareDrone('8', self.logger, 'blue', 'yellow')
        # self.swarm.addSoftwareDrone(droneEight)
        # self.socket.addSoftwareDrone(droneEight)

        # self.gps.start()
        self.socket.start()
        self.swarm.start()

        # self.swarm.connect()

        # while not self.swarm.isConnected():
        #     print("Connecting...")
        #     time.sleep(2)

        # print("Connected")

        # self.swarm.action = Action.Calibrate

        # while True:
        #     time.sleep(10)

        with Live(self.gui.layout, auto_refresh=False, screen=True) as live:
            while True:
                self.gui.key = self.key
                self.key = None

                if self.gui.state == State.Connecting:
                    if self.swarm.isConnected():
                        self.gui.state = State.Connected

                if self.swarm.action == None and self.gui.state == State.Kill:
                    self.gui.state = State.Connected

                if self.gui.action != None:
                    self.swarm.action = self.gui.action
                    self.gui.action = None

                self.gui.update()
                live.refresh()
                time.sleep(0.1)

        self.logger.info("End")

        self.gps.stop()
        self.socket.stop()

    def on_press(self, key):
        self.key = key