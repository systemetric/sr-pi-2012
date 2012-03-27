import time
import systemetric

def main():
    R = systemetric.Robot()
    while True:
        print "Reading markers"
        #Get only the tokens
        arenaMarkers = R.see(res=(1280,1024)).processed().arena
        
        # Are there any tokens?
        if arenaMarkers:
            nearest = min(arenaMarkers, key=lambda m: abs(m.center))
            R.driveTo(nearest.center, gap=0.2)
        else:
            print "No Marker..."
            
            # Spin 30 degrees clockwise
            R.rotateBy(30, fromTarget=True)
            
            # Disable heading correction
            R.stop()