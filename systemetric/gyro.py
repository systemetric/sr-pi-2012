from mbed import MbedDevice
from bearing import Bearing
import time

class Gyro(MbedDevice):
	def __init__(self, mbed = None):
		super(Gyro, self).__init__('G', mbed)

	@property
	def angularVelocity(self):
		return float(self.request('v'))
		
	@property
	def angle(self):
		return Bearing(float(self.request('a')))
		
	@angle.setter
	def angle(self, value):
		self.request('r', float(value))

	def startOffsetCalibration(self):
		self.request('o')
	
	def stopOffsetCalibration(self):
		self.request('o')

	def startScaleCalibration(self):
		self.request('s')

	def stopScaleCalibration(self, angleRotatedThrough):
		self.request('s', angleRotatedThrough)

def main():
	gyro = Gyro()
	gyro.startOffsetCalibration()
	time.sleep(5)
	gyro.stopOffsetCalibration()

	gyro.startScaleCalibration()
	print 'rotate the gyro 90 degrees'
	time.sleep(5)
	gyro.stopScaleCalibration(90)

	for i in xrange(20):
		try:
			print 'angular velocity: %f' % gyro.angularVelocity
			print 'angle: %f' % gyro.angle
			time.sleep(0.5)
		except:
			print 'failed'

	gyro.angle = 0

	for i in xrange(20):
		try:
			print 'angular velocity: %f' % gyro.angularVelocity
			print 'angle: %f' % gyro.angle
			time.sleep(0.5)
		except:
			print 'failed'