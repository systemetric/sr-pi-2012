from systemetric.compassrobot import *
import time

def main():
	R = CompassRobot()

    regulator = R.regulator

    regulator.ki = 0
    regulator.kd = 0
    regulator.target = 0

    for p in range(18, 25, 1):
    	regulator.kp = p / 10.0
    	print p / 10.0
    	regulator.enabled = True
    	time.sleep(5)
    	regulator.enabled = False
    	R.stop()
    	time.sleep(1)