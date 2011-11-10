import serial
import glob
import time

def main():
    port = serial.Serial('/dev/ttyACM0')
    port.open()
    port.timeout=0.25
    
    while True:
        line = port.readline()
        print line
    