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

import math
import time
import json

from libs.pyeuclid import Matrix4
from gyroandcompassrobot import GyroAndCompassRobot
from twowheeledrobot import AccessRevoked
from killablerobot import KillableRobot
from vision import VisionResult
from bearing import Bearing
from devices import Arm, Lifter, Ultrasonic
import logs
import threading

MAGIC_TURN_NUMBER = 1.2

class Robot(GyroAndCompassRobot, KillableRobot):
	'''A class derived from the base 'Robot' class provided by soton'''	 
	def __init__(self):
		#Get the motors set up
		GyroAndCompassRobot.__init__(self)

		with open('config.json') as configFile:
			KillableRobot.__init__(self, killCode = json.load(configFile).get('killCode') or 228)
		

		# Camera orientation - numbers need checking
		self.cameraMatrix = (
			Matrix4.new_translate(0, 0.48, 0) *     #0.5m up from the center of the robot
			Matrix4.new_rotatex(math.radians(18))   #Tilted forward by 18 degrees
		)

		# Cache, since .inverse is expensive
		self.worldTransform = self.cameraMatrix.inverse()

		#Set compass zero offset
		self.compass.heading = 0

		#get hardware
		self.arm    = Arm()
		self.lifter = Lifter()
		self.us     = Ultrasonic()

	def see(self, stats = False, *args, **kargs):
		"""
		Call the native see method, but return a VisionResult (a list with some
		extra members tacked on)
		"""

		res = KillableRobot.see(self, stats=stats, *args, **kargs)
		if stats:
			return VisionResult(res[0], worldTransform = self.worldTransform), res[1]
		else:
			return VisionResult(res, worldTransform = self.worldTransform)

	@logs.to(logs.movement)
	def driveDistance(self, distInMetres, speed = 100):
		"""
		Drive a certain distance forward in metres, using timing only. Negative
		distance goes backwards
		"""
		speed = abs(speed)
		print "Heading before:", self.compass.heading
		SPEED_AT_100 = .6	# we measured 3m in 5s
		self.drive(speed = math.copysign(speed, distInMetres))
		time.sleep(abs(distInMetres) / (SPEED_AT_100 * (speed / 100)))
		self.stop()
		print "Heading after:", self.compass.heading

	@logs.to(logs.movement)
	def turnToFace(self, relativePosition):
		bearing = float(Bearing.toPoint(relativePosition)) * MAGIC_TURN_NUMBER
		self.rotateBy(bearing)
		self.stop()
	
	@logs.to(logs.movement)
	def driveTo(self, relativePosition, gap = 0, speed = 100):
		bearing = float(Bearing.toPoint(relativePosition)) * MAGIC_TURN_NUMBER
		dist = abs(relativePosition) - gap
		print "Turning:", bearing
		self.rotateBy(bearing)
		self.stop()
		time.sleep(0.25)
		print "Driving:", dist
		self.driveDistance(dist, speed = speed)

	def executeUntilStart(self, f):
		def run():
			try:
				self.takeControl(kick=False)
				f(self)
			except AccessRevoked:
				print 'thread stopped'
		t = threading.Thread(target=run)
		t.start()
		self.waitForStart()
		self.takeControl()
