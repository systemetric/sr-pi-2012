from mbed import MbedDevice
import systemetric
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
		startTime = time.time()
		while wait and not self.atBottom and time.time() - startTime < 5:
			time.sleep(0.1)

	@property
	def atBottom(self):
		"""Bottom limit switches pressed?"""
		return 'True' in self.request('b') #atBottom

	@property
	def atTop(self):
		"""Bottom limit switches pressed?"""
		return 'True' in self.request('t') #atBottom

def main():
	A = Arm()
	R = systemetric.Robot()
	
	while True:
		time.sleep(3)
		A.grabCube(wait=True)
