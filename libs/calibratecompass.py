import time
import threading
from libs import compass

from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    R.compass.startCalibration()
    R.turn(8)
    time.sleep(20)
    R.compass.stopCalibration()
    R.stop()
    while True:
        print "bearing " + str(R.compass.heading)
        time.sleep(0.1)