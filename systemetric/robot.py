import sys
import math
import os
import time
import sr
from collections import namedtuple
import json

from libs.pyeuclid import *
from compassrobot import CompassRobot
from killablerobot import KillableRobot
from visionresult import VisionResult

from compass import Compass

config = json.load(open('config.json'))

Marker = namedtuple("Marker", "vertices normal location")
Markers = namedtuple("Markers", "tokens robots arena buckets")
Token = namedtuple("Token", "markers id timestamp location")

#info about the markers. Used in sr.vision
MarkerInfo = namedtuple( "MarkerInfo", "code marker_type offset size" )

DIE_HORRIBLY = config.get('killCode') or 228 #special marker

class Robot(CompassRobot, KillableRobot):
	'''A class derived from the base 'Robot' class provided by soton'''	 
	def __init__(self):
		#Get the motors set up
		CompassRobot.__init__(self)
		
		#set up the serial connection to the mbed
		try:
			self.compass = Compass()
		except Exception, c:
			self.end(message = str(c))
		
		#Camera orientation							
		self.cameraMatrix = Matrix4.new_rotate_euler(	# https://github.com/dov/pyeuclid/blob/master/euclid.txt (line 385)
			heading = 0,								 # rotation around the y axis
			attitude = -10,							  # rotation around the x axis
			bank = 0									 # rotation around the z axis
		)
		#Position and orientation of the robot
		self.robotMatrix = Matrix3()
	
   
	#deprecated
	@property 
	def compassHeading(self):
		return self.compass.heading

	def see(self, *args, **kargs):
		markers = KillableRobot.see(self, *args, **kargs)
		return VisionResult(markers)
	
	def driveDistance(self, distInMetres):
		SPEED = .575
		self.setSpeed(math.copysign(100, distInMetres))
		time.sleep(abs(distInMetres) / SPEED)
		self.stop()