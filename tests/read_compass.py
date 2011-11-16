import systemetric
import time
from systemetric.compass import Compass

def main():
	c = Compass()

	while True:
		print compass.heading
		time.sleep(0.1)