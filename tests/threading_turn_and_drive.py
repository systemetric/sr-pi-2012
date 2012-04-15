import systemetric
import threading
import time


robot = systemetric.Robot
def main(R):
	def spin():
		while True:
			R.rotateBy(20)
			time.sleep(1)

	def drive():
		while True:
			R.drive(40)
			time.sleep(3)
			R.drive(-40)

	driveR  = threading.Thread(target = drive)
	spinR = threading.Thread(target = spin)

	driveR.start()
	time.sleep(10)
	R.takeControl()
	R.power.beep(261, 1)
	spinR.start()
