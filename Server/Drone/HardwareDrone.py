from .Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFUALT_MASTER
from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.utils.power_switch import PowerSwitch

class HardwareDrone(Drone):
    def __init__(self, uri: str, color: str, master: bool = DEFUALT_MASTER):
        self.crazyflie = Crazyflie()
        self.powerSwitch = PowerSwitch(uri)
        self.motionCommander = MotionCommander(self.crazyflie)

        self.log_conf = LogConfig(name='data', period_in_ms=100)
        self.log_conf.add_variable('pm.vbat', 'float')
        self.log_conf.add_variable('pm.state', 'int8_t')
        self.log_conf.add_variable('range.zrange', 'uint16_t')
        self.log_conf.add_variable('sys.isFlying', 'uint8_t')
        self.log_conf.add_variable('sys.isTumbled', 'uint8_t')

        if master:
            self.log_conf.add_variable('range.back', 'uint16_t')
            self.log_conf.add_variable('range.front', 'uint16_t')
            self.log_conf.add_variable('range.left', 'uint16_t')
            self.log_conf.add_variable('range.right', 'uint16_t')
            self.log_conf.add_variable('range.up', 'uint16_t')

        super().__init__(uri, color, master)

    def connect(self) -> None:
        self.crazyflie.open_link(self.uri)

    def isConnected(self) -> bool:
        return self.crazyflie.is_connected()

    def kill(self) -> None:
        self.powerSwitch.stm_power_down()

    def addLogger(self) -> None:
        self.crazyflie.log.add_config(self.log_conf)
        self.log_conf.data_received_cb.add_callback(self.dataCallback)
        self.log_conf.start()

    def __dataCallback__(self, timestamp, data, logconf) -> None:
        self.data = data

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.take_off(height, velocity)

    def land(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.land(velocity)

    def stop(self) -> None:
        self.motionCommander.stop()

    def up(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_up(velocity)

    def down(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_down(velocity)

    def forward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_forward(velocity)

    def backward(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_back(velocity)

    def left(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_left(velocity)

    def right(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_right(velocity)

    def turnLeft(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_turn_left(velocity)

    def turnRight(self, velocity: float = DEFAULT_VELOCITY) -> None:
        self.motionCommander.start_turn_right(velocity)