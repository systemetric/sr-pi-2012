# This file is part of systemetric-student-robotics.

# systemetric-student-robotics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# systemetric-student-robotics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with systemetric-student-robotics.  If not, see <http://www.gnu.org/licenses/>.

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
		self.compassRegulator.kp =  2.75 # FIRST this number started at 0 and was raised until it started to oscillate
		self.compassRegulator.ki =  1.5  # THIRD we changed until it stopped dead on.
		self.compassRegulator.kd =  0.2  # SECOND we changed kd until the amount it overshot by was reduced

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
		self.speed = 0

		self.compassRegulator.enabled = True
		while not self.compassRegulator.onTarget(tolerance=tolerance):
			time.sleep(0.05)

	def rotateBy(self, angle, fromTarget = False, tolerance = 5):
		"""
		Rotate the robot a certain angle from the direction it is currently
		facing. Optionally rotate from the last target, preventing errors
		accumulating
		"""
		self.rotateTo((self.compassRegulator.target if fromTarget else self.compass.heading) + angle, tolerance = tolerance)
		
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