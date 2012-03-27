import serial
from bearing import Bearing
from mbed import MbedDevice

class Ultrasonic(MbedDevice):
	def __init__(self, mbed = None):
		super(Ultrasonic, self).__init__('U', mbed)
		self.distances = [float("nan")] * 4  

	def ping(self):
		self.distances = map(float, self.request().split())

	@property
	def front(self):
		return self.distances[0]
	
	@property
	def back(self):
		return self.distances[1]
	
	@property
	def left(self):
		return self.distances[2]
	
	@property
	def right(self):
		return self.distances[3]

def main():
	U = Ultrasonic()
	while True:
		U.ping()
		print U.front, U.back, U.left, U.right