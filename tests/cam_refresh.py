from sr import *
import time
import math
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    allMarkers = R.see()
    markers = [marker for marker in allMarkers if marker.info.marker_type == MARKER_TOKEN] #getting the valid QR code
    
    for i in range(21,0,-1):
        R.turn(i)
        time.pause(1.0)
        if len(markers) != 0:        #if there is A valid QR there...
            print "Found, speed of ",i
            R.power.beep([(440,1), (220,1)])