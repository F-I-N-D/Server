from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFAULT_RATE, DEFUALT_MASTER
from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.utils.power_switch import PowerSwitch
from Server.Logger.Logger import Logger

class HardwareDrone(Drone):
    def __init__(self, droneId: str, logger: Logger, color: str, master: bool = DEFUALT_MASTER):
        super().__init__(f'radio://0/20/2M/{droneId}', logger, color, master)
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
            self.log_conf.add_variable('range.up', 'uint16_t')
            self.log_conf.add_variable('range.front', 'uint16_t')
            self.log_conf.add_variable('range.back', 'uint16_t')
            self.log_conf.add_variable('range.left', 'uint16_t')
            self.log_conf.add_variable('range.right', 'uint16_t')


    def connect(self) -> None:
        super().connect()
        self.crazyflie.open_link(self.droneId)

    def isConnected(self) -> bool:
        super().isConnected()
        return self.crazyflie.is_connected()

    def disconnect(self) -> None:
        super().disconnect()
        self.crazyflie.close_link()

    def kill(self) -> None:
        super().kill()
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
        self.z = data['range.zrange'] / 10

        self.ldr = data['ExternalSensors.LDR']

        if self.master:
            self.distanceUp = data['range.up']
            self.distanceFront = data['range.front']
            self.distanceBack = data['range.back']
            self.distanceLeft = data['range.left']
            self.distanceRight = data['range.right']
        
        if self.isTumbled or self.isCharging:
            self.kill()

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        super().takeOff()
        self.motionCommander.take_off(height, velocity)

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().land()
        self.motionCommander.land(velocity)

    def stop(self) -> None:
        super().stop()
        self.motionCommander.stop()

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().up()
        self.motionCommander.start_up(velocity)

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().down()
        self.motionCommander.start_down(velocity)

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().forward()
        self.motionCommander.start_forward(velocity)

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().backward()
        self.motionCommander.start_back(velocity)

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().left()
        self.motionCommander.start_left(velocity)

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        super().right()
        self.motionCommander.start_right(velocity)

    def turnLeft(self, rate: float = DEFAULT_RATE) -> None:
        super().turnLeft()
        self.motionCommander.start_turn_left(rate)

    def turnRight(self, rate: float = DEFAULT_RATE) -> None:
        super().turnRight()
        self.motionCommander.start_turn_right(rate)