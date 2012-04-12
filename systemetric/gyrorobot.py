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

		#PID settings
		self.compassRegulator.kp = 1.500 # FIRST this number started at 0 and was raised until it started to oscillate
		self.compassRegulator.ki = 0.175 # THIRD we changed until it stopped dead on.
		self.compassRegulator.kd = 0.080 # SECOND we changed kd until the amount it overshot by was reduced

		#PID settings
		self.gyroRegulator.kp = 0.0   # FIRST this number started at 0 and was raised until it started to oscillate
		self.gyroRegulator.ki = 0.0   # THIRD we changed until it stopped dead on.
		self.gyroRegulator.kd = 0.0   # SECOND we changed kd until the amount it overshot by was reduced
		self.gyroRegulator.target = 0

		self.compassRegulator.start()
		self.gyroRegulator.start()

		self.speed = 0

	@logs.to(logs.movement)
	def driveStraight(self, speed):
		self.compassRegulator.enabled = False

		self.speed = speed

		self.gyroRegulator.enabled = True
		
	def rotateTo(self, angle):
		self.gyroRegulator.enabled = False

		self.compassRegulator.target = angle
		self.speed = 0

		self.compassRegulator.enabled = True
		
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

		R.driveStraight(50)
		time.sleep(5)
		R.stop()

CompassAndGyroRobot = GyroAndCompassRobot