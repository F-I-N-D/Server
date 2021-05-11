from Server.Drone.Drone import Drone, DEFAULT_HEIGHT, DEFAULT_VELOCITY, DEFUALT_MASTER
from cflib.crazyflie import Crazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.log import LogConfig
from cflib.utils.power_switch import PowerSwitch

class HardwareDrone(Drone):
    def __init__(self, id: str, color: str, master: bool = DEFUALT_MASTER):
        super().__init__(f'radio://0/20/2M/{id}', color, master)

        self.crazyflie = Crazyflie()
        self.powerSwitch = PowerSwitch(self.id)
        self.motionCommander = MotionCommander(self.crazyflie)

        self.log_conf = LogConfig(name='data', period_in_ms = 500)
        self.log_conf.add_variable('pm.vbat', 'float')
        self.log_conf.add_variable('pm.state', 'int8_t')
        self.log_conf.add_variable('sys.isFlying', 'uint8_t')
        self.log_conf.add_variable('sys.isTumbled', 'uint8_t')
        self.log_conf.add_variable('range.zrange', 'uint16_t')
        self.log_conf.add_variable('sensor.ldr', 'uint16_t')

        if master:
            self.log_conf.add_variable('range.up', 'uint16_t')
            self.log_conf.add_variable('range.front', 'uint16_t')
            self.log_conf.add_variable('range.back', 'uint16_t')
            self.log_conf.add_variable('range.left', 'uint16_t')
            self.log_conf.add_variable('range.right', 'uint16_t')


    def connect(self) -> None:
        print(self.id)
        self.crazyflie.open_link(self.id)

    def isConnected(self) -> bool:
        print(self.crazyflie.is_connected())
        print(self.crazyflie.state)
        print(self.crazyflie.connected_ts)
        return self.crazyflie.is_connected()

    def kill(self) -> None:
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
        self.z = data['range.zrange']

        if self.master:
            self.distanceUp = data['range.up']
            self.distanceFront = data['range.front']
            self.distanceBack = data['range.back']
            self.distanceLeft = data['range.left']
            self.distanceRight = data['range.right']
        
        if self.isTumbled:
            self.kill()

    def takeOff(self, height: float = DEFAULT_HEIGHT, velocity: float = DEFAULT_VELOCITY) -> None:
        if not self.isCharging:
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