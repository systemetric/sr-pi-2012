from mbed import MbedDevice
import time

class Gyro(MbedDevice):
	def __init__(self, mbed = None):
		super(Gyro, self).__init__('G', mbed)

	@property
	def angularVelocity(self):
		return float(self.request('v'))

	def calibrate(self):
		self.request('c')

def main():
	gyro = Gyro()
	gyro.calibrate()

	while 1:
		print "Angular Velocity:", gyro.angularVelocity
		time.sleep(0.1)