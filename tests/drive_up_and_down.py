from sr import *
import time
import math
import systemetric

def main():
    forward = True
    R = systemetric.Robot()
    initialAngle = R.compass.heading
    R.rotateTo(initialAngle)
    while True:
        R.driveDistance(1 if forward else -1)
        R.rotateBy(60, fromTarget=True)
        markers = R.see()
        R.rotateBy(60, fromTarget=True)
        markers = R.see()
        R.rotateBy(60, fromTarget=True)
        time.sleep(0.5)

        forward = not forward