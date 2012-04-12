import os, time, sys, functools, inspect, time, collections, threading, contextlib, itertools

_robotStarted = time.time()
_roundStarted = None

# class ThreadedOutputStream(object):
# 	def __init__(self, inner):
# 		self.streams = collections.defaultdict(lambda: inner)

# 	@property
# 	def stream(self): return self.streams[threading.current_thread()]
# 	@stream.setter
# 	def stream(self, s): self.streams[threading.current_thread()] = s
# 	@stream.deleter
# 	def stream(self): del self.streams[threading.current_thread()]

# 	def write(self, data):
# 		self.stream.write(data)

class StreamWrapper(object):
	"""
	Wraps a stream, and buffers it line at a time, to allow messages to be
	appended or prepended to
	"""
	def __init__(self, stream):
		self.stream = stream
		self.line = ''

	def write(self, data):
		"""Called when print is used"""
		if '\n' in data:
			lines = data.split('\n')
			lines[0] = self.line + lines[0]
			lines, self.line = lines[:-1], lines[-1]
			for line in lines:
				self.writeLine(line)
		else:
			self.line += data

	def writeLine(self, data):
		"""Write one line to the stream. Called by write(). Override in derived classes"""
		if isinstance(self.stream, StreamWrapper):
			self.stream.writeLine(data)
		else:
			self.stream.write(data + '\n')

	def wraps(self, stream):
		"""Check if this stream wraps another stream"""
		return self == stream or isinstance(self.stream, StreamWrapper) and self.stream.wraps(stream) or self.stream == stream

class MirroringStream(StreamWrapper):
	"""
	Mirrors the output of one stream to another, adding a prefix to the second
	with the name of the first
	"""
	def __init__(self, stream, name, to):
		super(MirroringStream, self).__init__(stream)
		self.name = name
		self.to = to

	def writeLine(self, line):
		super(MirroringStream, self).writeLine(line)
		self.to.writeLine(self.name + ':\t' + line)


class TimestampedLogger(StreamWrapper):
	"""
	Adds the round time in seconds to the start of every line
	"""
	def __init__(self, stream):
		super(TimestampedLogger, self).__init__(stream)

	def writeLine(self, data):
		if _roundStarted:
			t = '@%.1f ' % (time.time() - _roundStarted)
		else:
			t = '#%.1f ' % (time.time() - _robotStarted)

		super(TimestampedLogger, self).writeLine(t + data)

class IndentingLogger(StreamWrapper):
	"""
	Indents each line by a certain number of tabs
	"""
	def __init__(self, stream, indent = 0):
		super(IndentingLogger, self).__init__(stream)
		self.indent = indent

	def writeLine(self, data):
		super(IndentingLogger, self).writeLine('\t'*self.indent + data)

	@property
	@contextlib.contextmanager
	def indented(self):
		self.indent += 1
		yield
		self.indent -= 1



_timestamp = time.strftime("%Y-%m-%d %H.%M.%S", time.gmtime())
logsdir = os.path.join('/mnt/user/', 'custom-logs', _timestamp)

try:
	os.makedirs(logsdir)
except:
	pass

sys.stdout = IndentingLogger(TimestampedLogger(sys.stdout))
movement = IndentingLogger(MirroringStream(TimestampedLogger(open(os.path.join(logsdir, 'movement.txt'), 'w')), name='movement', to=sys.stdout))
events   = IndentingLogger(MirroringStream(TimestampedLogger(open(os.path.join(logsdir, 'events.txt'  ), 'w')), name='event',    to=sys.stdout))
errors   = IndentingLogger(MirroringStream(TimestampedLogger(open(os.path.join(logsdir, 'errors.txt'  ), 'w')), name='error',    to=sys.stdout))
vision   = IndentingLogger(MirroringStream(TimestampedLogger(open(os.path.join(logsdir, 'errors.txt'  ), 'w')), name='vision',   to=sys.stdout))

def roundStarted():
	"""Start the round timer"""
	global _roundStarted
	_roundStarted = time.time()

_makeArgList = lambda args, kargs: (
	', '.join(itertools.chain(
		(repr(arg) for arg in args),
		('%s=%s' % (k, repr(v)) for k, v in kargs.iteritems())
	))
)

@contextlib.contextmanager
def redirectedOutput(o):
	"""Redirects stdout to point to another stream, within the scope of a with - NOT THREAD SAFE!"""
	old = sys.stdout
	if not old.wraps(o):
		sys.stdout = o
	yield
	sys.stdout = old

def to(log):
	def decorator(f):
		"""Redirects prints, and logs the function invocation"""
		
		if 'self' in inspect.getargspec(f).args:
 			def wrapped(self, *args, **kargs):
				with redirectedOutput(log):
					print '%s.%s(%s)' % (self.__class__.__name__, f.__name__, _makeArgList(args, kargs))
					with sys.stdout.indented:
						result = f(self, *args, **kargs)
						if result: print "returned", result

				return result
 		else:
			def wrapped(*args, **kargs):
				with redirectedOutput(log):
					print '%s(%s)' % (f.__name__, _makeArgList(args, kargs))
					with sys.stdout.indented:
						result = f(*args, **kargs)
						if result: print "returned", result

				return result
		return functools.wraps(f)(wrapped)
	return decorator


def main():
	print >> movement, "Hello"
	print "test"
	print "test"
	print "test"
	print "test"
	print >> movement, "World"
	print >> movement, "World"
	print >> movement, "World"
	print >> movement, "World"

	
	class test(object):
		@to(movement)
		def it(self, p, q):
			print "Bar"
			return 5

		@property
		@to(movement)
		def that(self):
			pass

		@that.setter
		@to(movement)
		def that(self, value):
			print 10+value

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
	t.it(3, "4")
	time.sleep(1)
	print t.that
	time.sleep(1)
	t.that = 7
	print t.that