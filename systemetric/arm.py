from mbed import MbedDevice
import time

class Arm(MbedDevice):
	"""
	A class to control the arm via the mbed. The arm has two control wires - a
	blue one, which causes the arm to move when pulled to 0V (through a FET),
	and a yellow one, which is pulled to 0V when the bottom limit switches are pressed.
	"""
	def __init__(self, mbed = None):
		super(Arm, self).__init__('A', mbed)

	def grabCube(self, wait = True):
		self.request('g') #grab

		while wait and not self.atBottom:
			time.sleep(0.1)

	@property
	def atBottom(self):
		"""Bottom limit switches pressed?"""
		self.request('b') #atBottom
