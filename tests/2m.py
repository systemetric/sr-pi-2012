from sr import *
import time
import systemetric

def main():
	R = systemetric.Robot()

	R.driveDistance(2)
	R.stop()
	time.sleep(2)
	R.rotateBy(180)
	R.driveDistance(2)
	R.stop()