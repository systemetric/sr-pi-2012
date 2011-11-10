import serial
import glob
import time
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    port = serial.Serial('/dev/ttyACM0')
    port.open()
    port.timeout=0.25
    angle = 90000 #random value
    
    while angle > 10:
        angle = float(port.readline())
        print angle
        time.sleep(0.25)
    print 'We finished!'
    R.turn(0)
    