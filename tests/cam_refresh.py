from sr import *
import time
import math
import systemetric

def main():
    res = (320, 240)
    R = systemetric.Robot()
    
    
   # markers = [marker for marker in allMarkers if marker.info.marker_type == MARKER_TOKEN] #getting the valid QR code
    while True:
        markers = R.see(res=res)
        if len(markers) != 0:
            break
        R.power.beep(440,1)
        
    for i in range(21,0,-1):
        R.turn(i)
        time.sleep(1)
        markers = R.see( res=(640, 360) )
        if len(markers) != 0:        #if there is A valid QR there...
            print "Found, speed of ",i
            R.power.beep([(440,1), (220,1)])
            break
    R.stop()
   