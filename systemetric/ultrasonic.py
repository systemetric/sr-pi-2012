import serial
from bearing import Bearing
from mbed import Mbed

class Ultrasonic(object):
	def __init__(self, mbed = None):
		self.mbed = mbed or Mbed.get()
		self.distances = [float("nan")] * 4  

	def ping(self):
		distances = self.mbed.sendCommand('U').split()
		self.distances = map(float, distances)

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