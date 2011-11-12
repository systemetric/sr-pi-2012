from sr import *
import time
import math
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    speed = 50
    
    while True:
        #Get only the tokens
        allMarkers = R.see()
        markers = [marker for marker in allMarkers if marker.info.marker_type == MARKER_TOKEN] #filtering the valid QR codes
        time.sleep(0.05)
        if len(markers) != 0:        #if there is A valid QR there...
            R.stop()
            print "Saw the marker"
            angle = markers[0].centre.polar.rot_y    #set the angle of the object (from center)
            if math.fabs(angle) < 10:                #set angle to an absolute value, then drive @ angle
                R.setSpeed(speed)
            else:                                    #else, stop
                R.rotateBy(angle)
                time.sleep(0.25)
                R.stop()
            print "seen at: ",angle
        else:
            R.rotateBy(10)
            print "No Marker..."