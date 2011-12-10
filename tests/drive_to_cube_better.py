from sr import *
import time
import math
import systemetric

def main():
    R = systemetric.Robot()


    while True:
        print "Reading markers"
        #Get only the tokens
        allMarkers = R.see(res=(1280,1024))
        
        markers = allMarkers.tokens
        
        # Are there any tokens?
        if markers:
            #Get the angle of the token
            for marker in markers:
                angle = marker.centre.polar.rot_y
                
                print "Marker seen at: ", angle
                
                R.rotateBy(angle)
                print "Facing marker"
                # Drive forward almost the distance to the marker
                R.driveDistance(marker.dist-0.1)

                break
        else:
            print "No Marker..."
            
            # Spin 30 degrees clockwise
            R.rotateBy(30, fromTarget=True)
            
            # Disable heading correction
            R.stop()