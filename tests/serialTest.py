import serial
import glob
import time
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    port = serial.Serial('/dev/ttyACM0')
    port.open()
    port.timeout=0.25
    angle = 200 #random value
    
    while angle > 3:
        angle = float(port.readline())
        print angle
        R.turn(15)
        time.sleep(1)
    