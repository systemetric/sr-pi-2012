import math
import time
import json

from libs.pyeuclid import Matrix4
from compassrobot import CompassRobot
from killablerobot import KillableRobot
from vision import VisionResult
from bearing import Bearing
from lifter import Lifter
from arm import Arm
import logs
import threading

class AccessRevoked(Exception):
	"""Thrown when a thread attempts to control the robot after its access has been revoked"""
	pass

class SingleThreadAccess(object):
	"""
	Allow only one thread access to the resource at a time. At any time a
	thread can grab control, causing attribute access in other threads to throw
	an exception, revoking control from the others. Base class members can
	still be accessed through super.
	"""
	def __init__(self):
		self.owner = threading.current_thread()

	def __getattribute__(self, attr):
		if attr not in ('owner', 'takeControl', 'hasControl') and not self.hasControl:
			raise AccessRevoked
		return super(SingleThreadAccess, self).__getattribute__(attr)

	def takeControl(self):
		"""Take control of the object, revoking access to all other threads"""
		self.owner = threading.current_thread()

	@property
	def hasControl(self):
		"""
		Check if the current thread has control - not required in user code.
		Daemon threads, such as the PID, always have access
		"""
		return self.owner == threading.current_thread() or threading.current_thread().daemon

class Robot(CompassRobot, KillableRobot, SingleThreadAccess):
	'''A class derived from the base 'Robot' class provided by soton'''	 
	def __init__(self):
		#Get the motors set up
		CompassRobot.__init__(self)

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
		print "\tRobot.driveDistance(%.2f)" % distInMetres
		print "\t\tHeading before:", self.compass.heading
		SPEED = .6	# we measured 3m in 5s
		self.drive(speed = math.copysign(100, distInMetres))
		time.sleep(abs(distInMetres) / SPEED)
		self.stop()
		print "\t\tHeading after:", self.compass.heading

	@logs.to(logs.movement)
	def turnToFace(self, relativePosition):
		print "\tRobot.turnToFace(%s)" % relativePosition
		bearing = Bearing.toPoint(relativePosition)
		print "\t\tTurning:", bearing
		self.rotateBy(bearing)
		self.stop()
	
	@logs.to(logs.movement)
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
