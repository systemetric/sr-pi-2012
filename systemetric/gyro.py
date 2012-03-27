from mbed import MbedDevice

class Gyro(MbedDevice):
	def __init__(self, mbed = None):
		super(Gyro, self).__init__('G', mbed)

	@property
	def angularVelocity(self):
		return float(self.request('v'))
		
	@property
	def angle(self):
		return float(self.request('a'))
		
	@angle.setter
	def angle(self, value):
		return float(self.request('r', value))

	def startOffsetCalibration(self):
		self.request('o')
	
	def stopOffsetCalibration(self):
		self.request('o')

	def startScaleCalibration(self):
		self.request('s')

	def stopScaleCalibration(self, angleRotatedThrough):
		self.request('s', angleRotatedThrough)