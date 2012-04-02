from mbed import MbedDevice

class LaserGate(MbedDevice):
	"""
	A class to read the laser light gate via the mbed. The laser needs to be
	powered with 3.3V from the mbed, and some kind of light detector should be
	hooked up as well. Might be a good idea to only turn the laser on when the
	sensor is checked.
	"""
	def __init__(self, mbed = None):
		super(LaserGate, self).__init__('L', mbed)

	@property
	def blocked(self):
		return bool(self.request())
		#TODO: Maybe have the mbed return a float so that this code can decide
		#      what the definition of "blocked" is
