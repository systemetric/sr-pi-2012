import systemetric
import threading
import pick_up_cubes
import bucket
import time


robot = systemetric.Robot
def main(R):
	findCubes  = threading.Thread(target = lambda: (R.takeControl(), pick_up_cubes.main(R)))
	findBucket = threading.Thread(target = lambda: (R.takeControl(), bucket.main(R)))

	#start finding cubes
	findCubes.start()
	time.sleep(20)

	R.takeControl()
	R.power.beep(261, 1)

	#Switch to bucket finding
	findBucket.start()
