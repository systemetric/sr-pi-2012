import serial
from bearing import Bearing
from mbed import Mbed

class Gyro(object):
	def __init__(self, mbed = None):
		self.mbed = mbed or Mbed.get()

	@property
	def angle(self):
		return float(self.mbed.sendCommand('Ga'))

	@property
	def angularVelocity(self):
		return float(self.mbed.sendCommand('Gv'))

	def startOffsetCalibration(self):
		self.mbed.sendCommand('Go')
	
	def stopOffsetCalibration(self):
		self.mbed.sendCommand('Go')

	def startScaleCalibration(self):
		self.mbed.sendCommand('Gs')

	def stopScaleCalibration(self, angleRotatedThrough):
		self.mbed.sendCommand('Gs')
		self.mbed.sendCommand(struct.pack(s, angleRotatedThrough))