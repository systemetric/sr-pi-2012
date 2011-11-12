from sr import *
import time
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    R.drive(100)
    time.sleep(10)
    R.stop()
    time.sleep(10)
    
    R.drive(75)
    time.sleep(10)
    R.stop()
    time.sleep(10)
    
    R.drive(50)
    time.sleep(10)
    R.stop()
    time.sleep(10)
    
    R.drive(25)
    time.sleep(10)
    
    R.stop()