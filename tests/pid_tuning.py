from systemetric.compassrobot import *
import time

def main():
    regulator = CompassRobot().regulator

    regulator.ki = 0
    regulator.kd = 0
    regulator.target = 0

    for p in range(1.8, 2.2, 0.1):
    	regulator.kp = p
    	print p
    	regulator.enabled = True
    	time.sleep(5)
    	regulator.enabled = False
    	time.sleep(1)