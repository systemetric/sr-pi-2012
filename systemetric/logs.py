import os, time, sys

_robotStarted = time.time()
_roundStarted = None

_originalOut = sys.stdout

class TimestampedLogger():
	def __init__(self, name, stream):
		self.stream = stream
		self.name = name

	def write(self, data):
		if _roundStarted:
			t = '@%.1f' % (time.time() - _roundStarted)
		else:
			t = '#%.1f' % (time.time() - _robotStarted)

		print >> self.stream, t, data
		print self.name+':', data

_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

logsdir = os.getcwd()  #os.path.join('/mnt/user/', 'custom-logs', timestamp)

movement = TimestampedLogger('movement', open(os.path.join(logsdir, 'movement.txt'), 'w'))
events = TimestampedLogger('event', open(os.path.join(logsdir, 'events.txt'), 'w'))
errors = TimestampedLogger('error', open(os.path.join(logsdir, 'errors.txt'), 'w'))
vision = TimestampedLogger('vision', open(os.path.join(logsdir, 'errors.txt'), 'w'))

sys.stdout = TimestampedLogger(sys.stdout)

def roundStarted():
	global _roundStarted
	_roundStarted = time.time()