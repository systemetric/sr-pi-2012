import sr
import os, sys

class KillableRobot(sr.Robot):
	"""An abstraction that allows a robot to be killed when a certain marker is seen"""
	def __init__(self, killCode):
		self.killCode = killCode
		sr.vision.marker_luts['dev'][killCode] = sr.vision.MarkerInfo(
			code = killCode,
			marker_type = None,
			offset = None,
			size = 1 #Errors if 0
		)
	
	def see(self, stats = False, *args, **kw):
		"""Intercept Robot.see, and kill the robot if the killCode is seen"""
		res = sr.Robot.see(self, stats = stats, *args, **kw)

		if stats:
			markers = res[0]
			stats = res[1]
		else:
			markers = res

		for marker in markers:
			if marker.info.code == self.killCode:
				self.end("Terminated by marker %d" % self.killCode, error=False)
			   
		return markers, stats if stats else markers

		
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