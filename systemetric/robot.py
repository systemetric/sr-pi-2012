import math
import time
import json

from libs.pyeuclid import Matrix4
from compassrobot import CompassRobot
from killablerobot import KillableRobot
from vision import VisionResult
from bearing import Bearing

class Robot(CompassRobot, KillableRobot):
	'''A class derived from the base 'Robot' class provided by soton'''	 
	def __init__(self):
		#Get the motors set up
		CompassRobot.__init__(self)

		with open('config.json') as configFile:
			KillableRobot.__init__(self, killCode = json.load(configFile).get('killCode') or 228)
		
		# Camera orientation - numbers need checking
		self.cameraMatrix = (
			Matrix4.new_translate(0, 0.5, 0) *      #0.5m up from the center of the robot
			Matrix4.new_rotatex(math.radians(10))   #Tilted forward by 10 degrees
		)

		# Cache, since .inverse is expensive
		self.worldTransform = self.cameraMatrix.inverse()

		#Set compass zero offset
		self.compass.heading = 0

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

	def driveDistance(self, distInMetres):
		"""
		Drive a certain distance forward in metres, using timing only. Negative
		distance goes backwards
		"""
		print "\tRobot.driveDistance(%.2f)" % distInMetres
		print "\t\tHeading before:", self.compass.heading
		SPEED = .575
		self.drive(speed = math.copysign(100, distInMetres))
		time.sleep(abs(distInMetres) / SPEED)
		self.stop()
		print "\t\tHeading after:", self.compass.heading

	def turnToFace(self, relativePosition):
		print "\tRobot.turnToFace(%s)" % relativePosition
		bearing = Bearing.toPoint(relativePosition)
		print "\t\tTurning:", bearing
		self.rotateBy(bearing)
		self.stop()
	
	def driveTo(self, relativePosition, gap = 0):
		bearing = Bearing.toPoint(relativePosition)
		dist = abs(relativePosition) - gap
		print "Robot.driveTo:"
		print "\tTurning:", bearing
		self.rotateBy(bearing)
		self.stop()
		time.sleep(0.25)
		print "\tDriving:", dist
		self.driveDistance(dist)
