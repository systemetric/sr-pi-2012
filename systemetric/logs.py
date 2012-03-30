import os, time, sys, functools, inspect, time

_robotStarted = time.time()
_roundStarted = None

_originalOut = sys.stdout

class TimestampedLogger():
	def __init__(self, stream, name=''):
		self.stream = stream
		self.name = name
		self.newLine = True

	def write(self, data):
		if self.newLine:
			if _roundStarted:
				t = '@%.1f' % (time.time() - _roundStarted)
			else:
				t = '#%.1f' % (time.time() - _robotStarted)

			self.stream.write(t + ' ')
			if self.name: sys.stdout.write(self.name + ': ')

		self.stream.write(data)
		if self.name: sys.stdout.write(data)

		self.newLine = data[-1] == '\n'

	def __getattr__(self, attr): 
		return getattr(self.stream, attr) 


_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

logsdir = 'V:\\' #os.getcwd()  #os.path.join('/mnt/user/', 'custom-logs', timestamp)
print os.path.join(logsdir, 'movement.txt')
movement = TimestampedLogger(open(os.path.join(logsdir, 'movement.txt'), 'w'), 'movement')
events   = TimestampedLogger(open(os.path.join(logsdir, 'events.txt'  ), 'w'), 'event')
errors   = TimestampedLogger(open(os.path.join(logsdir, 'errors.txt'  ), 'w'), 'error')
vision   = TimestampedLogger(open(os.path.join(logsdir, 'errors.txt'  ), 'w'), 'vision')

sys.stdout = TimestampedLogger(sys.stdout)

def roundStarted():
	global _roundStarted
	_roundStarted = time.time()

def to(log):
	"""Create a decorator that makes a function log it's argument to a file"""
	def decorator(f):
		"""Decorator for functions"""
		method = 'self' in inspect.getargspec(f).args
		name = f.__name__

		def logit(args, kargs, result, self = None):
			arglist = ', '.join(str(arg) for arg in args)
			if kargs: 
				arglist += ', '
				arglist += ', '.join('%s=%s' % (k, v) for k, v in kargs.iteritems())

			msg = '%s(%s)'% (name, arglist)
			if self:
				msg = self.__class__.__name__ + '.' + msg
			if result:
				msg += '->' + str(result)
			print >> log, msg

		if method:
			def wrapped(self, *args, **kargs):
				result = f(self, *args, **kargs)
				logit(args, kargs, result, self)
				return result
		else:
			def wrapped(*args, **kargs):
				result = f(*args, **kargs)
				logit(args, kargs, result)
				return result
		return functools.wraps(f)(wrapped)
	return decorator


def main():
	print >> movement, "Hello"
	print "test"
	print >> movement, "World"

	class test():
		@to(movement)
		def it(self, p, q):
			print "Bar"
			return 5
		@property
		@to(movement)
		def that(self):
			return 3

	t = test()

	@to(movement)
	def move(x, y):
		print "Foo"
		return (6, 7, 85)

	move(1, 2)
	time.sleep(1)
	roundStarted()
	t.it(3, 4)
	time.sleep(1)
	print t.that