import time
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    target = 0
    
    while True:
        heading = R.compassHeading
        print heading
        time.sleep(0.2)