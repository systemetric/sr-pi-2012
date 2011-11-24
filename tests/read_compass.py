import systemetric
import time
from systemetric.compass import Compass

def main():
	compass = Compass()

	while True:
		print compass.heading
		time.sleep(0.1)