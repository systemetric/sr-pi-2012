import time
import systemetric

def main():
    R = systemetric.Robot()
    while True:
        print "Reading markers"
        #Get only the tokens
        tokens = R.see(res=(1280,1024)).processed().tokens
        
        # Are there any tokens?
        if tokens:
            R.driveTo(tokens[0].center, gap=0.2)
            R.arm.grabCube(wait = False);
            time.sleep(3)
            R.driveDistance(-0.5)
        else:
            print "No Marker..."
            
            # Spin 30 degrees clockwise
            R.rotateBy(30, fromTarget=True)
            
            # Disable heading correction
            R.stop()