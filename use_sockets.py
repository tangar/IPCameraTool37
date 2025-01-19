
from MySocket import *
from endoscope import *

import time
import keyboard

eds = Endoscope()

tx = TxSocket()
tx.Open('192.168.37.2', 9999)

sock = RxSocket(callback=eds.MessageProcessor)
sock.Open('', 9998)

tx.Send(bytes([Commands.CMD_PING.value]))
tx.Send(bytes([Commands.CMD_GET_DEVICE_INFO.value]))
tx.Send(bytes([Commands.CMD_GET_STATUS.value]))

eds.bottomLight.PWM = 128
eds.bottomLight.Freq = 20000

def prepBotLight(pwm, freq):
    b0 = Commands.CMD_SET_BOTTOM_LIGHT_BRIGHTNESS.value
    b1 = pwm % 256
    b2 = freq % 256
    b3 = freq // 256
    return b0,b1,b2,b3

while True:
    time.sleep(0.1) 
    if keyboard.is_pressed('q'):
        print("Вы нажали: 'q'")
        break

    if keyboard.is_pressed('p'):
        b0, b1, b2, b3 = prepBotLight(eds.bottomLight.PWM, eds.bottomLight.Freq)
        tx.Send(bytes([b0, b1, b2, b3]))
        print ("Вы нажали P")
