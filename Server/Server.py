import logging
import time
import cflib.crtp
from pynput import keyboard
from rich.live import Live

from Server.Swarm.Swarm import Swarm, Action
from Server.GPS.GPS import GPS
from Server.Socket.Socket import Socket
from Server.Drone.HardwareDrone import HardwareDrone
from Server.Drone.SoftwareDrone import SoftwareDrone
from Server.Logger.Logger import Logger
from Server.Logger.Level import Level
from Server.Gui.Gui import Gui, State

# The id's of the drones
idMaster = 'E7E7E7E700'
idOne = 'E7E7E7E701'
idTwo = 'E7E7E7E702'
idThree = '3'
idFour = '4'
idFive = '5'

logging.basicConfig(level=logging.INFO)

class Server:
    # Institiate all the classes
    def __init__(self):
        self.logger = Logger(Level.Info)
        self.gui = Gui()
        self.gps = GPS()
        self.socket = Socket(8000)
        self.swarm = Swarm(self.logger)
        self.listener = keyboard.Listener(on_press = self.on_press)
        self.key = None

    # Start the server
    def start(self) -> None:
        self.logger.addGui(self.gui)
        self.logger.info("Start")
        cflib.crtp.init_drivers()
        self.listener.start()

        # Create all drones and add them to the neede classes
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

        droneEight = SoftwareDrone('8', self.logger, 'blue', 'yellow')
        self.swarm.addSoftwareDrone(droneEight)
        self.socket.addSoftwareDrone(droneEight)

        # Start all services
        # self.gps.start()
        self.socket.start()
        self.swarm.start()

        # self.swarm.action = Action.Connect

        # while not self.swarm.isConnected():
        #     print("Connecting...")
        #     time.sleep(1)

        # print("Connected")

        # self.swarm.action = Action.Search

        # while True:
        #     time.sleep(10)

        running = True

        # Start running the GUI
        with Live(self.gui.layout, auto_refresh=False, screen=True) as live:
            while running:
                self.gui.key = self.key
                self.key = None

                if self.gui.state == State.Connecting:
                    if self.swarm.isConnected():
                        self.gui.state = State.Actions

                if self.gui.action != Action.Null:
                    self.swarm.action = self.gui.action
                    self.gui.action = Action.Null

                if self.swarm.action == Action.Null and self.gui.state == State.FlyingOperations:
                    self.gui.state = State.Actions

                running = self.gui.update()
                live.refresh()
                time.sleep(0.1)

        self.logger.info("End")

        self.gps.stop()
        self.socket.stop()
        self.swarm.stop()

    def on_press(self, key):
        self.key = key