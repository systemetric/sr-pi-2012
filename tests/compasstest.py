import time
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    target = 0
    
    while True:
        heading = R.compassHeading
        
        error = heading - target
        while error >= 180:
            error -= 360
        while error < -180:
            error += 360
            
        print heading
        R.turn(error/3)
        time.sleep(0.2)