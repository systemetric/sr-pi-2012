from compassrobot import TwoWheeledRobot
from gyro import Gyro
from compass import Compass
from pid import PID
from arm import Arm
import time
import logs

class GyroAndCompassRobot(TwoWheeledRobot):
	def __init__(self):
		super(GyroAndCompassRobot, self).__init__()

		self.gyro = Gyro()
		self.compass = Compass()

		self.compassRegulator = PID(
			getInput = lambda: self.compass.heading,
			setOutput = lambda x: TwoWheeledRobot.drive(self, speed = 0, steer = x),
			outputRange = (-100, 100),
			iLimit = 0.25
		)
		self.gyroRegulator = PID(
			getInput = lambda: self.gyro.angularVelocity,
			setOutput = lambda x: TwoWheeledRobot.drive(self, speed = self.speed, steer = x),
			outputRange = (-100, 100),
			iLimit = 0.25
		)
		#self.regulator.tuneFromZieglerNichols(2.575, 0.698)

		#Compass PID settings
		self.compassRegulator.kp = 1.500 # FIRST this number started at 0 and was raised until it started to oscillate
		self.compassRegulator.ki = 0.175 # THIRD we changed until it stopped dead on.
		self.compassRegulator.kd = 0.080 # SECOND we changed kd until the amount it overshot by was reduced

		#Gyro PID settings
		self.gyroRegulator.kp = 3   # FIRST this number started at 0 and was raised until it started to oscillate
		self.gyroRegulator.ki = 7.5 # THIRD we changed until it stopped dead on.
		self.gyroRegulator.kd = 0   # SECOND we changed kd until the amount it overshot by was reduced
		self.gyroRegulator.target = 0


		self.compassRegulator.start()
		self.gyroRegulator.start()

		self.speed = 0

	@logs.to(logs.movement)
	def drive(self, speed, steer = 0, regulate = True):
		"""
		Drive the robot at a certain speed, by default using the compass to
		regulate the robot's heading.

		TODO: Tune PID controller for straight movement.
		"""
		if regulate:
			self.compassRegulator.enabled = False

			self.speed = speed
			self.gyro.calibrate()
			self.gyroRegulator.target = steer
			self.gyroRegulator.enabled = True
		else:
			TwoWheeledRobot.drive(self, speed, steer)

	@logs.to(logs.movement)	
	def rotateTo(self, angle, tolerance = 5):
		self.gyroRegulator.enabled = False
		self.compassRegulator.target = angle
		print "started"
		self.speed = 0

		self.compassRegulator.enabled = True
		print "started"
		while not self.compassRegulator.onTarget(tolerance=tolerance):
			time.sleep(0.05)
		print "stopped"

	def rotateBy(self, angle, fromTarget = False):
		"""
		Rotate the robot a certain angle from the direction it is currently
		facing. Optionally rotate from the last target, preventing errors
		accumulating
		"""
		self.rotateTo((self.compassRegulator.target if fromTarget else self.compass.heading) + angle)
		
	def stop(self):
		"""
		Stop the robot, by setting the speed to 0, and disabling regulation
		"""
		self.speed = 0
		self.gyroRegulator.enabled = False
		self.compassRegulator.enabled = False
		super(GyroAndCompassRobot, self).stop()

def main():
	R = GyroAndCompassRobot()
	A = Arm()
	while True:
		while not A.atTop:
			pass
		while A.atTop:
			pass

		R.drive(100)
		time.sleep(5)
		R.stop()

		time.sleep(0.5)

		R.rotateBy(180)
		R.stop()
		time.sleep(0.5)


		R.drive(50)
		time.sleep(5)
		R.stop()

		time.sleep(0.5)


CompassAndGyroRobot = GyroAndCompassRobot