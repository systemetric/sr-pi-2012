import time

class Timer(object):
	class EventTimer(object):
		def __init__(self, timer, name):
			self.timer = timer
			self.name = name

		def __enter__(self):
			self.start = time.time()

		def __exit__(self, t, v, tb):
			self.timer.times[self.name] = time.time() - self.start
			return False

	def __init__(self):
		self.reset()

	def time(self, name):
		return Timer.EventTimer(self, name)

	def reset(self):
		self.times = {}

