import time
from systemetric import Robot

def main():
    R = Robot()
    
    R.compass.startCalibration()
    R.turn(8)
    time.sleep(20)
    R.compass.stopCalibration()
    R.stop()
    while True:
        print "bearing " + str(R.compass.heading)
        time.sleep(0.1)