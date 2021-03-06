from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.utils.power_switch import PowerSwitch

from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFAULT_RATE, DEFUALT_MASTER
from Server.Logger.Logger import Logger

class HardwareDrone(Drone):
    def __init__(self, droneId: str, logger: Logger, colorFront: str, colorBack: str, master: bool = DEFUALT_MASTER):
        super().__init__(f'radio://0/20/2M/{droneId}', logger, colorFront, colorBack, master)
        self.crazyflie = Crazyflie()
        self.powerSwitch = PowerSwitch(self.droneId)
        self.motionCommander = MotionCommander(self.crazyflie)

        self.log_conf = LogConfig(name='data', period_in_ms = 100)
        self.log_conf.add_variable('pm.vbat', 'float')
        self.log_conf.add_variable('pm.state', 'int8_t')
        self.log_conf.add_variable('sys.isFlying', 'uint8_t')
        self.log_conf.add_variable('sys.isTumbled', 'uint8_t')
        self.log_conf.add_variable('range.zrange', 'uint16_t')
        self.log_conf.add_variable('ExternalSensors.LDR', 'float')

        if master:
            self.log_conf.add_variable('range.front', 'uint16_t')
            self.log_conf.add_variable('range.back', 'uint16_t')
            self.log_conf.add_variable('range.left', 'uint16_t')
            self.log_conf.add_variable('range.right', 'uint16_t')

    # Connect to the drone by opening crazyflie link
    def connect(self) -> None:
        super().connect()
        self.crazyflie.open_link(self.droneId)

    # Check if the drone is connected and connect the logger if it is connected
    def isConnected(self) -> bool:
        super().isConnected()
        if self.crazyflie.is_connected():
            self.crazyflie.log.add_config(self.log_conf)
            self.addLogger()

        return self.crazyflie.is_connected()

    def disconnect(self) -> None:
        super().disconnect()
        self.crazyflie.close_link()

    # Kill the drone by shutting of the power
    def kill(self, message: str) -> None:
        super().kill(message)
        self.powerSwitch.stm_power_down()
        self.disconnect()
        print("killed", message, self.droneId)

    def restartLogger(self):
        self.removeLogger()
        self.addLogger()

    # Add a logger and his callback
    def addLogger(self) -> None:
        self.log_conf.data_received_cb.add_callback(self.dataCallback)
        self.log_conf.start()

    # Add a logger and his callback
    def removeLogger(self) -> None:
        self.log_conf.data_received_cb.remove_callback(self.dataCallback)

    # Save data on data callback
    def dataCallback(self, timestamp, data, logconf) -> None:
        self.batteryVoltage = data['pm.vbat']
        self.isCharging = True if data['pm.state'] == 1 else False

        self.isFlying = True if data['sys.isFlying'] == 1 else False
        self.isTumbled = True if data['sys.isTumbled'] == 1 else False

        self.distanceDown = data['range.zrange']
        self.locationZ = int(data['range.zrange'] / 10)

        self.ldr = data['ExternalSensors.LDR']
        print(self.droneId, self.ldr)

        if self.master:
            self.distanceFront = int(data['range.front'] / 10)
            self.distanceBack = int(data['range.back'] / 10)
            self.distanceLeft = int(data['range.left'] / 10)
            self.distanceRight = int(data['range.right'] / 10)

        super().dataCallback(data)

    # Take off to predefined height
    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> bool:
        if not super().takeOff(height, velocity):
            return False
        self.motionCommander.take_off(height / 100, velocity)
        return True

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().land(velocity)
        self.motionCommander.land(velocity)

    def stop(self) -> None:
        super().stop()
        self.motionCommander.stop()

    # Hove in the direction of the target by adjusting the velocity
    def move(self, velocityX: float, velocityY: float, velocityZ: float, rate: float) -> None:
        super().move(velocityX, velocityY, velocityZ, rate)
        self.motionCommander._set_vel_setpoint(velocityX, velocityY, velocityZ, rate)