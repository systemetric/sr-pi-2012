from sr import *
import time
import math
from systemetricRobot import SystemetricRobot

R = SystemetricRobot()

speed = 50

while True:
    markers = R.see()
    if len(markers) != 0:
        print "Saw the marker"
        targetPoint = markers[0].centre
        R.right = speed + targetPoint.polar.rot_y
        R.left = speed - targetPoint.polar.rot_y
    else:
        print "No marker"
        R.right = 0
        R.left = 0
        
    time.sleep(0.1)