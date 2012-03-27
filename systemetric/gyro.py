import serial
from bearing import Bearing
from mbed import MbedDevice

class Gyro(MbedDevice):
	def __init__(self, mbed = None):
		super(Ultrasonic, self).__init__('G', mbed)

	@property
	def angle(self):
		return float(self.request('a'))

	@property
	def angularVelocity(self):
		return float(self.request('v'))

	def startOffsetCalibration(self):
		self.request('o')
	
	def stopOffsetCalibration(self):
		self.request('o')

	def startScaleCalibration(self):
		self.request('s')

	def stopScaleCalibration(self, angleRotatedThrough):
		self.request('s')
		self.request(angleRotatedThrough)