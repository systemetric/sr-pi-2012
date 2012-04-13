import math
import time
import json

from libs.pyeuclid import Matrix4
from gyroandcompassrobot import GyroAndCompassRobot
from killablerobot import KillableRobot
from vision import VisionResult
from bearing import Bearing
from lifter import Lifter
from arm import Arm
from ultrasonic import Ultrasonic
import logs

class Robot(GyroAndCompassRobot, KillableRobot):
	'''A class derived from the base 'Robot' class provided by soton'''	 
	def __init__(self):
		#Get the motors set up
		GyroAndCompassRobot.__init__(self)
		logs.roundStarted()

		with open('config.json') as configFile:
			KillableRobot.__init__(self, killCode = json.load(configFile).get('killCode') or 228)
		

		# Camera orientation - numbers need checking
		self.cameraMatrix = (
			Matrix4.new_translate(0, 0.48, 0) *      #0.5m up from the center of the robot
			Matrix4.new_rotatex(math.radians(18))   #Tilted forward by 18 degrees
		)

		# Cache, since .inverse is expensive
		self.worldTransform = self.cameraMatrix.inverse()

		#Set compass zero offset
		self.compass.heading = 0

		self.arm = Arm()
		self.lifter = Lifter()
		self.us = Ultrasonic()

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
	def driveDistance(self, distInMetres):
		"""
		Drive a certain distance forward in metres, using timing only. Negative
		distance goes backwards
		"""
		print "Heading before:", self.compass.heading
		SPEED = .6	# we measured 3m in 5s
		self.drive(speed = math.copysign(100, distInMetres))
		time.sleep(abs(distInMetres) / SPEED)
		self.stop()
		print "Heading after:", self.compass.heading

	@logs.to(logs.movement)
	def turnToFace(self, relativePosition):
		bearing = Bearing.toPoint(relativePosition)
		self.rotateBy(bearing)
		self.stop()
	
	@logs.to(logs.movement)
	def driveTo(self, relativePosition, gap = 0):
		bearing = Bearing.toPoint(relativePosition)
		dist = abs(relativePosition) - gap
		print "Turning:", bearing
		self.rotateBy(bearing)
		self.stop()
		time.sleep(0.25)
		print "Driving:", dist
		self.driveDistance(dist)
