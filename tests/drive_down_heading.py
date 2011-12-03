from sr import *
import systemetric
import time

def main():
	R = systemetric.Robot()
	speed = 25
	R.rotateTo(R.compass.heading)
	R.setSpeed(speed)
	time.sleep(1)