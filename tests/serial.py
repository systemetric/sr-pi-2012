import serial
import time

def main():
    port = serial.Serial('/dev/ttyACM0')
    
    port.open()
    port.timeout=0.25
    
    while True:
        port.write('H')
        angle = int(port.readline()) / 10.0
        print angle
        time.sleep(0.2)