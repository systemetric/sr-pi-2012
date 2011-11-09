from sr import *
import time
import math
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    
   # markers = [marker for marker in allMarkers if marker.info.marker_type == MARKER_TOKEN] #getting the valid QR code
    
    for i in range(21,0,-1):
        R.turn(i)
        time.sleep(1)
        markers = R.see( res=(640, 360) )
        if len(markers) != 0:        #if there is A valid liboki there...
            print "Found, speed of ",i
            R.power.beep([(440,1), (220,1)])
            break
    R.stop()
   