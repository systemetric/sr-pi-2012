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
        R.rotateBy(60, fromTarget=True)
        R.rotateBy(60, fromTarget=True)

        forward = not forward