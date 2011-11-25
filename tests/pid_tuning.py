from systemetric.compassrobot import *
import time
from tests.gui.slider import * 

def main():
	R = CompassRobot()

	regulator = R.regulator

	window = PIDWindow(regulator)
	window.runInBackground()

	regulator.ki = 0
	regulator.kd = 0
	regulator.target = 0

	regulator.kp = 1
	regulator.enabled = True
	time.sleep(30)
	regulator.enabled = False
	R.stop()
	R.power.beep([(440, 0.5)])

	regulator.enabled = True
	time.sleep(60)
	regulator.enabled = False
	R.stop()

	#for p in range(18, 25, 1):
	#	regulator.kp = p / 10.0
	#	print p / 10.0
	#	regulator.enabled = True
	#	time.sleep(5)
	#	regulator.enabled = False
	#	R.stop()
	#	time.sleep(1)