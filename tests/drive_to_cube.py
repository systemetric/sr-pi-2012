from sr import *
import time
import math
from systemetricRobot import SystemetricRobot

def main():
    R = SystemetricRobot()
    
    speed = 50
    
    while True:
        #Get only the tokens
        markers = [marker for marker in R.see() if marker.info.marker_type == MARKER_TOKEN]
        
        if len(markers) != 0:
            print "Saw the marker"
            angle = markers[0].centre.polar.rot_y
            if math.fabs(angle) < 10:
                R.drive(speed)
            else:
                R.left = angle
                R.right = -angle
                time.sleep(0.25)
                R.stop()
            
            print(angle)
        else:
            print "No marker"
            R.drive(steer=5)
            time.sleep(0.25)
            R.stop()