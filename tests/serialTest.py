import serial
import glob
import time

port = serial.Serial('/dev/ttyACM0')
port.open()
port.timeout=0.25
    
while True:
    print port.readline()