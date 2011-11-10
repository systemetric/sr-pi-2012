import serial
import glob
import time
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    port = serial.Serial('/dev/ttyACM0')
    
    port.open()
    port.timeout=0.25
    
    while True:
        port.write('H')
        angle = int(port.readline()) / 10.0
        print angle
        time.sleep(0.2)