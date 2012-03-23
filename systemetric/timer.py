import time
import sys
class Timer(object):
	def __init__(self, name = "Timer", parent = None, printTo = sys.stdout):
		self.parent = parent
		self.name = name
		self.reset()
		self.time = 0
		self.printTo = printTo

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
		return Timer(name, self, printTo=self.printTo)

	def reset(self):
		self.times = []

	def toTimeTree(self, indent = 0):
		print >> self.printTo, '\t' * indent + '%s: %f' % (self.name, self.time)
		for child in self.times:
			child.toTimeTree(indent+1)

def main():
	with Timer("profiling", printTo = open(r'test.txt', 'w')) as t:
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