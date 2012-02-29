import systemetric
import pickle
import time
import os

def main():
	R = systemetric.Robot()
	t = time.strftime("%d %b %Y %H.%M.%S", time.gmtime())
	directory = os.path.join(R.usbkey, t)
	if not os.path.isdir(directory):
		os.mkdir(directory)

	for i in range(20):
		vision = R.see()

		filename = os.path.join(directory, 'visionResult{0}.dat'.format(i))

		with open(filename, 'w') as f:
			pickle.dump(vision, f)
		
		R.power.beep(440, 1)
		time.sleep(5)