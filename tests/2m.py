from sr import *
import systemetric

def main():
	R = systemetric.robot()

	R.driveDistance(2)
	R.stop()
	R.rotateBy(180)
	R.driveDistance(2)
	R.stop()