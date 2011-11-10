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
        angle = int(port.readline()) / 10
        print angle
        time.sleep(0.2)    