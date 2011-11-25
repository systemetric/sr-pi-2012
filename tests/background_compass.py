from systemetric.compassrobot import *
import time

def main():
    R = CompassRobot()
    R.regulator.tuneFromZieglerNichols(2.575, 0.698)
    R.rotateTo(0)
    time.sleep(1)
    '''print "rotated to 0:", R.compass.heading
    time.sleep(1)
    R.rotateBy(90)
    time.sleep(1)
    print "rotated by 90:", R.compass.heading
    time.sleep(1)
    R.rotateBy(-180)
    time.sleep(1)
    print "rotated by -180:", R.compass.heading
    R.regulate = False
    R.stop()
    print "stopped:", R.compass.heading'''