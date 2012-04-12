import systemetric
import time

R = systemetric.twowheeledrobot.TwoWheeledRobot()
A = systemetric.arm.Arm()

def waitForSignal(delay=0.1):
	while not A.atTop:
		pass
	while A.atTop:
		pass
	time.sleep(delay)

def main():
	print "Voltage before\tvoltage during\tMotor power"
	for i in xrange(0, 100, 10):
		waitForSignal()
		v = R.power.battery.voltage

		R.drive(speed=100)
		time.sleep(0.1)
		R.drive(speed=i)
		time.sleep(2.5)
		print "%.2f\t%2f\t%d" % (v, R.power.battery.voltage, i)
		time.sleep(2.5)
		R.stop()
