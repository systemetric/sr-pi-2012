import json
import sr

import os, sys

config = json.load(open('config.json'))

DIE_HORRIBLY = config.get('killCode') or 228 #special marker

def KillableRobot(self):
	def __init__(self):
		sr.vision.marker_luts['dev'][DIE_HORRIBLY] = sr.vision.MarkerInfo(
			code = DIE_HORRIBLY,
			marker_type = None,
			offset = None,
			size = 1 #Errors if 0
		)
	
	def see(self, *args, **kw):
		markers = sr.Robot.see(self, *args, **kw)
		for marker in markers:
			if marker.info.code == DIE_HORRIBLY:
				self.end("Terminated by marker %d" % DIE_HORRIBLY, error=False)
			   
		return markers

		
	def end(self, message = 'robot stopped', error = True, shutdown = False):
		'''Kill the robot in the nicest way possible'''
		print message
		
		#stop the motors
		self.stop()
		#beep if error
		if error:
			self.power.beep([(440, 1), (220, 1), (880, 1)])
		else:
			self.power.beep([(262,2), (440, 2),(524, 2)])	
		#end the program with an exit code
		if shutdown:
			os.system('shutdown -P now')
		else:
			sys.exit(int(error))