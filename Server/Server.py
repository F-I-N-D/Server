import sys
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

logging.basicConfig(level=logging.ERROR)

class Server:
    # Institiate all the classes
    def __init__(self, droneFile: str, camera: int, noGui: str):
        self.logger = Logger(Level.Info)
        self.gui = Gui()
        self.gps = GPS(camera)
        self.socket = Socket(8000)
        self.swarm = Swarm(self.logger)
        self.listener = keyboard.Listener(on_press = self.on_press)
        self.key = None
        self.noGui = noGui
        self.droneFile = droneFile

    # Start the server
    def start(self) -> None:
        self.logger.addGui(self.gui)
        self.logger.info("Start")
        cflib.crtp.init_drivers()
        self.listener.start()

        self.__setDrones()      

        # Start all services
        self.gps.start()
        self.socket.start()
        self.swarm.start()

        if self.noGui:
            self.swarm.action = Action.Connect

            while not self.swarm.isConnected():
                print("Connecting...")
                time.sleep(1)

            print("Connected")

            if self.noGui == "search":
                self.swarm.action = Action.Search
            elif self.noGui == "calibrate":
                self.swarm.action = Action.Calibrate
            elif self.noGui == "scatter":
                self.swarm.action = Action.Scatter

            while True:
                time.sleep(10)
        else:
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

    # Load all drones from the specified file
    def __setDrones(self):
        try:
            f = open(self.droneFile, "r")
        except:
            raise Exception("Drone file does not exists")
            sys.exit()

        data = f.readlines()
        for droneValue in data:
            if droneValue.startswith("#"):
                continue
            
            droneValue = droneValue.strip()
            splittedValue = droneValue.split(',')

            if splittedValue[0] == 'H':
                drone = HardwareDrone(splittedValue[1], self.logger, splittedValue[2], splittedValue[3], splittedValue[4] == "True")
                self.swarm.addHardwareDrone(drone)
                self.gps.addDrone(drone)
                self.socket.addHardwareDrone(drone)
            elif splittedValue[0] == 'S':
                drone = SoftwareDrone(splittedValue[1], self.logger, splittedValue[2], splittedValue[3], splittedValue[4] == "True")
                self.swarm.addSoftwareDrone(drone)
                self.socket.addSoftwareDrone(drone)