import time
import json
class Timer(object):
	def __init__(self, name = "Timer", parent = None):
		self.parent = parent
		self.name = name
		self.reset()
		self.time = 0

	def __enter__(self):
		self.start = time.time()
		return self

	def __exit__(self, t, v, tb):
		self.time = time.time() - self.start

		if self.parent:
			self.parent.times += [self]
		else:
			self.toTimeTree()
		return False

	def event(self, name):
		return Timer(name, self)

	def reset(self):
		self.times = []

	def toTimeTree(self, indent = 0):
		print '\t' * indent + '%s: %f' % (self.name, self.time)
		for child in self.times:
			child.toTimeTree(indent+1)

def main():
	with Timer("profiling") as t:
		with t.event("a") as a:
			time.sleep(1)

			with a.event("b"):
				time.sleep(0.1)
			with a.event("bb") as b:
				time.sleep(0.1)
				with b.event("ebb"):
					time.sleep(0.1)
			with a.event("bbb"):
				time.sleep(0.1)

		with t.event("c"):
			time.sleep(0.2)

	