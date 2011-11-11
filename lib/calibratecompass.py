import time
import threading
from lib import compass

from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    R.compass.startCalibration()
    R.turn(10)
    time.sleep(20)
    R.compass.stopCalibration()
    R.stop()
    while True:
        print "bearing "+R.compass.heading
        time.sleep(1)