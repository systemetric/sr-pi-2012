import os, time, sys, functools, inspect, time, collections, threading

_robotStarted = time.time()
_roundStarted = None

class StreamWrapper(object):
	def __init__(self, stream):
		self.stream = stream

	def wraps(self, stream):
		return self.stream == stream or isinstance(self.stream, StreamWrapper) and self.stream.wraps(stream)


class ThreadedOutputStream(object):
	def __init__(self, inner):
		super(ThreadedOutputStream, self).__setattr__('streams', collections.defaultdict(lambda: inner))

	@property
	def stream(self): return self.streams[threading.current_thread()]
	@stream.setter
	def stream(self, s): self.streams[threading.current_thread()] = s
	@stream.deleter
	def stream(self): del self.streams[threading.current_thread()]

	def write(self, data):
		self.stream.write(data)

class LineBufferedStream(StreamWrapper):
	def __init__(self, stream):
		super(LineBufferedStream, self).__init__(stream)
		self.line = ''

	def writeLine(self, data):
		self.stream.write(data)

	def write(self, data):
		self.line += data

		if data[-1] == '\n':
			self.writeLine(self.line)
			self.line = ''

class TimestampedLogger(LineBufferedStream):
	def __init__(self, stream, name=''):
		super(TimestampedLogger, self).__init__(stream)
		self.name = name

	def writeLine(self, data):
		if _roundStarted:
			t = '@%.1f ' % (time.time() - _roundStarted)
		else:
			t = '#%.1f ' % (time.time() - _robotStarted)

		self.stream.write(t + data)
		if self.name: _stdout.write(self.name + ':\t' + data)

	def __getattr__(self, attr): 
		return getattr(self.stream, attr)

class IndentingLogger(LineBufferedStream):
	def __init__(self, stream, indent):
		super(IndentingLogger, self).__init__(stream)
		self.indent = indent

	def writeLine(self, data):
		self.stream.write('\t'*self.indent + data)


sys.stdout = TimestampedLogger(sys.stdout)
_stdout = sys.stdout
sys.stdout = ThreadedOutputStream(sys.stdout)

_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

logsdir = 'V:\\' #os.getcwd()  #os.path.join('/mnt/user/', 'custom-logs', timestamp)
movement = TimestampedLogger(open(os.path.join(logsdir, 'movement.txt'), 'w'), 'movement')
events   = TimestampedLogger(open(os.path.join(logsdir, 'events.txt'  ), 'w'), 'event')
errors   = TimestampedLogger(open(os.path.join(logsdir, 'errors.txt'  ), 'w'), 'error')
vision   = TimestampedLogger(open(os.path.join(logsdir, 'errors.txt'  ), 'w'), 'vision')


def roundStarted():
	global _roundStarted
	_roundStarted = time.time()

def to(log):
	"""Create a decorator that makes a function log it's argument to a file"""
	def decorator(f):
		"""Decorator for functions"""
		method = 'self' in inspect.getargspec(f).args
		name = f.__name__

		def logit(args, kargs, self = None):
			arglist = ', '.join(str(arg) for arg in args)
			if kargs: 
				arglist += ', '
				arglist += ', '.join('%s=%s' % (k, v) for k, v in kargs.iteritems())

			msg = '%s(%s):'% (name, arglist)
			if self:
				msg = self.__class__.__name__ + '.' + msg
			#if result:
			#	msg += '->' + str(result)
			print msg

		if method:
			def wrapped(self, *args, **kargs):
				oldStream = sys.stdout.stream

				if not oldStream.wraps(log): sys.stdout.stream = log
				
				logit(args, kargs, self)
				
				sys.stdout.stream = IndentingLogger(sys.stdout.stream, 1)
				
				result = f(self, *args, **kargs)
				if result: print 'returned %s' % str(result)

				sys.stdout.stream = oldStream
				return result
		else:
			def wrapped(*args, **kargs):
				oldStream = sys.stdout.stream
				if not oldStream.wraps(log):
					sys.stdout.stream = log

				logit(args, kargs)
				
				sys.stdout.stream = IndentingLogger(sys.stdout.stream, 1)

				result = f(*args, **kargs)
				if result: print 'returned %s' % str(result)
				sys.stdout.stream = oldStream
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
		print "Baz"

		return move2(56,342)

	@to(movement)
	def move2(x, y):
		print "Foo"
		return (6, 7, 85)

	move(1, 2)
	time.sleep(1)
	roundStarted()
	t.it(3, 4)
	time.sleep(1)
	print t.that

main()