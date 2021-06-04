from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFAULT_RATE, DEFUALT_MASTER
from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.utils.power_switch import PowerSwitch
from Server.Logger.Logger import Logger

class HardwareDrone(Drone):
    def __init__(self, droneId: str, logger: Logger, colorFront: str, colorBack: str, master: bool = DEFUALT_MASTER):
        super().__init__(f'radio://0/20/2M/{droneId}', logger, colorFront, colorBack, master)
        self.crazyflie = Crazyflie()
        self.powerSwitch = PowerSwitch(self.droneId)
        self.motionCommander = MotionCommander(self.crazyflie)

        self.log_conf = LogConfig(name='data', period_in_ms = 50)
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

    def connect(self) -> None:
        super().connect()
        self.crazyflie.open_link(self.droneId)

    def isConnected(self) -> bool:
        super().isConnected()
        if self.crazyflie.is_connected():
            self.logger.info("Connected", self.droneId)
            self.addLogger()

        return self.crazyflie.is_connected()

    def disconnect(self) -> None:
        super().disconnect()
        self.crazyflie.close_link()

    def kill(self, message: str) -> None:
        super().kill(message)
        self.powerSwitch.stm_power_down()

    def addLogger(self) -> None:
        self.crazyflie.log.add_config(self.log_conf)
        self.log_conf.data_received_cb.add_callback(self.__dataCallback)
        self.log_conf.start()

    def __dataCallback(self, timestamp, data, logconf) -> None:
        self.batteryVoltage = data['pm.vbat']
        self.isCharging = True if data['pm.state'] == 1 else False

        self.isFlying = True if data['sys.isFlying'] == 1 else False
        self.isTumbled = True if data['sys.isTumbled'] == 1 else False

        self.distanceDown = data['range.zrange']
        self.locationZ = int(data['range.zrange'] / 10)

        self.ldr = data['ExternalSensors.LDR']

        if self.master:
            self.distanceFront = data['range.front']
            self.distanceBack = data['range.back']
            self.distanceLeft = data['range.left']
            self.distanceRight = data['range.right']
        
        if self.isTumbled:
            self.kill("Tumbled")
        elif self.isCharging:
            self.kill("Charging")

        if self.batteryVoltage < 2.8 and self.batteryVoltage > 0.0:
            self.kill("Battery low", self.droneId)
            self.disconnect()

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        super().takeOff(height, velocity)
        if self.batteryVoltage < 3.5 and self.batteryVoltage > 0.0:
            self.logger.warning("Battery low", self.droneId)
            self.disconnect()
            return

        self.motionCommander.take_off(height, velocity)

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().land(velocity)
        self.motionCommander.land(velocity)

    def stop(self) -> None:
        super().stop()
        self.motionCommander.stop()

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().up(velocity)
        self.motionCommander.start_up(velocity)

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().down(velocity)
        self.motionCommander.start_down(velocity)

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().forward(velocity)
        self.motionCommander.start_forward(velocity)

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().backward(velocity)
        self.motionCommander.start_back(velocity)

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().left(velocity)
        self.motionCommander.start_left(velocity)

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().right(velocity)
        self.motionCommander.start_right(velocity)

    def turnLeft(self, rate: float = DEFAULT_RATE) -> None:
        super().turnLeft(rate)
        self.motionCommander.start_turn_left(rate)

    def turnRight(self, rate: float = DEFAULT_RATE) -> None:
        super().turnRight(rate)
        self.motionCommander.start_turn_right(rate)

    def move(self, velocityX: float, velocityY: float, velocityZ: float, rate: float) -> None:
        super().move(velocityX, velocityY, velocityZ, rate)
        self.motionCommander._set_vel_setpoint(velocityX, velocityY, velocityZ, rate)