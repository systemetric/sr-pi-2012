from sr import *
import time
import math
import systemetric

def main():
    R = systemetric.Robot()

    while True:
        #Get only the tokens
        allMarkers = R.see()
        markers = [marker for marker in allMarkers if marker.info.marker_type == MARKER_TOKEN]
        
        # Are there any tokens?
        if markers:
            #Get the angle of the token
            angle = markers[0].centre.polar.rot_y
            
            print "Marker seen at: ", angle
            
            R.rotateBy(angle)
            
            # Drive forward almost the distance to the marker
            R.driveDistance(markers[0].dist-0.3)
        else:
            print "No Marker..."
            
            # Spin 20 degrees clockwise
            R.rotateBy(20)
            
            # Disable heading correction
            R.stop()