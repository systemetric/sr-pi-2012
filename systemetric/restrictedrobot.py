import threading, time

class AccessRevoked(Exception):
	pass

class SingleThreadAccess(object):
	def __init__(self):
		self.owner = threading.current_thread()

	def __getattribute__(self, attr):
		if attr not in ('owner', 'takeControl', 'hasControl') and not self.hasControl:
			raise AccessRevoked
		return super(SingleThreadAccess, self).__getattribute__(attr)

	def takeControl(self):
		self.owner = threading.current_thread()

	@property
	def hasControl(self):
		return self.owner == threading.current_thread()

class Test1(object):
	def __init__(self):
		SingleThreadAccess.__init__(self)
		self.y = 2
	def bar(self):
		print self.y

class Test(Test1, SingleThreadAccess):
	x = 1
	a = 2

t = Test()

def foo():
	t.takeControl()
	print "new", t.x

t2=threading.Thread(target=foo)

try:
	print t.x
	print t.a
	t2.start()
	time.sleep(2)
	Test1.bar(t)
	t.bar()
	print t.a
except AccessRevoked:
	print "Lost access to the robot"