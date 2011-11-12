from lib.compassrobot import *

def main():
    R = CompassRobot()
    print R.compass.heading
    R.rotateBy(30)
    print R.compass.heading
    R.rotateBy(-30)
    R.regulate = False