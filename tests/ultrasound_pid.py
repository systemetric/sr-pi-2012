from systemetric.pid import PID
import time

def main(R):
	print "Help!"
	regulator = PID(
		getInput = lambda: R.us.ping() or R.us.front,
		setOutput = lambda x: R.drive(x),
		outputRange = (-100, 100),
		iLimit = 0.25
	)
	#regulator.tuneFromZieglerNichols(2.575, 0.698)

	#PID settings
	regulator.kp = 50 #3.2 #1.500 # FIRST this number started at 0 and was raised until it started to oscillate
	regulator.ki = 0 #0.175 # THIRD we changed until it stopped dead on.
	regulator.kd = 0 #0.194 #0.080 # SECOND we changed kd until the amount it overshot by was reduced
	regulator.target = 0.5

	regulator.enabled = True

	regulator.start()

	while True:
		time.sleep(10)