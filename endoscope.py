from enum import Enum

class Commands(Enum):
    CMD_PING = 1
    CMD_GET_DEVICE_INFO = 2
    CMD_GET_STATUS = 3
    CMD_SET_BOTTOM_LIGHT_BRIGHTNESS = 4
    CMD_SET_SIDE_LIGHT_BRIGHTNESS = 5
    CMD_SET_MOTOR_MAX_CURRENT = 6

class Light:
    def __init__(self, PWM = 0, Freq = 0, Status = 0, Current = 0):
        self.PWM = PWM
        self.Freq = Freq
        self.Status = Status
        self.Current = Current

class Motor:
    def __init__(self, CURRENT_limit, CURRENT_now = 0, target_pwm = 0, current_pwm = 0, Status = 0):
        self.CURRENT_limit = CURRENT_limit
        self.CURRENT_now = CURRENT_now
        self.target_pwm = target_pwm
        self.current_pwm = current_pwm
        self.Status = Status

class Endoscope:
    def __init__(self):
        self.sideLight = Light()
        self.bottomLight = Light()
        self.motor = Motor 
        self.TemperatureSide = 0
        self.TemperatureUC = 0
        self.id = 0
        self.hw = 0
        self.sw = 0
        self.alive = 0
    
    def MessageProcessor(self, data, addr):
        rxLen = len(data)
        id = data[0]

        if (id == 1):
            self.alive = True
            print(f"CMD_PING")

        elif (id == 2):
            self.id = data[0+1]
            self.hw = data[1+1]
            self.sw = data[2+1]
            print(f"CMD_GET_DEVICE_INFO ID = {self.id} HW = {self.hw} FW = {self.sw}")
        
        elif (id == 3):
            self.TemperatureSide = data[17 + 1]
            self.TemperatureUC = data[18 + 1]
            print(f"CMD_GET_STATUS LED: {self.TemperatureSide} UC: {self.TemperatureUC}")
        
        else:
            print(f"Получено сообщение: {id} длиной {rxLen} от {addr}.")
            print("сообщение не обработано")

    def prepBotLight(pwm, freq):
        b0 = Commands.CMD_SET_BOTTOM_LIGHT_BRIGHTNESS.value
        b1 = pwm % 256
        b2 = freq % 256
        b3 = freq // 256
        return b0,b1,b2,b3
        
        
        