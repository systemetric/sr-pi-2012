from systemetric.gyrorobot import *
import time
from tests.gui.slider import * 

def main():
	R = GyroRobot()

	R.gyro.startOffsetCalibration()
	time.sleep(5)
	R.gyro.stopOffsetCalibration()

	R.gyro.startScaleCalibration()
	print 'rotate the gyro 90 degrees'
	time.sleep(5)
	R.gyro.stopScaleCalibration(90)

	regulator = R.regulator
	regulator.kp  = 0
	regulator.ki = 0
	regulator.kd = 0
	regulator.target = 0
	
	window = PIDWindow(regulator)
	window.runInBackground()


	regulator.enabled = True

	#for p in range(18, 25, 1):
	#	regulator.kp = p / 10.0
	#	print p / 10.0
	#	regulator.enabled = True
	#	time.sleep(5)
	#	regulator.enabled = False
	#	R.stop()
	#	time.sleep(1)