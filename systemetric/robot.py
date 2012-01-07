import math
import time
import json

import libs.pyeuclid as pyeuclid
from compassrobot import CompassRobot
from killablerobot import KillableRobot
from visionresult import VisionResult
from bearing import Bearing

class Robot(CompassRobot, KillableRobot):
	'''A class derived from the base 'Robot' class provided by soton'''	 
	def __init__(self):
		#Get the motors set up
		CompassRobot.__init__(self)

		with open('config.json') as configFile:
			KillableRobot.__init__(self, killCode = json.load(configFile).get('killCode') or 228)
		
		# Camera orientation, using yaw, pitch, and roll
		self.cameraMatrix = pyeuclid.Matrix4.new_rotate_euler(  
			heading = 0,    #yaw
			attitude = 0, #math.degrees(-10), #pitch
			bank = 0        #roll
		)
		# Cache, since .inverse is expensive
		self.worldTransform = self.cameraMatrix.inverse()

		#Set compass zero offset
		self.compass.initializeZeroOffset()
	
	#deprecated
	@property 
	def compassHeading(self):
		return self.compass.heading

	def see(self, *args, **kargs):
		"""
		Call the native see method, but return a VisionResult (a list with some
		extra members tacked on)
		"""
		markers = KillableRobot.see(self, *args, **kargs)
		return VisionResult(markers, worldTransform = self.worldTransform)
	
	def driveDistance(self, distInMetres):
		"""
		Drive a certain distance forward in metres, using timing only. Negative
		distance goes backwards
		"""
		SPEED = .575
		self.drive(speed = math.copysign(100, distInMetres))
		time.sleep(abs(distInMetres) / SPEED)
		self.stop()
	
	def driveTo(self, relativePosition, gap = 0):
		self.rotateBy(Bearing.toPoint(relativePosition))
		self.driveDistance(abs(relativePosition) - gap)
