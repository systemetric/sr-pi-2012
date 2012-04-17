# This file is part of systemetric-student-robotics.

# systemetric-student-robotics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# systemetric-student-robotics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with systemetric-student-robotics.  If not, see <http://www.gnu.org/licenses/>.

class Event:
	"""
	A simple event system.

	.. code-block:: python

		e = Event()
		def onFired(x)
			print "Fired with", x
		e += onFired
		e('go') #prints "Fired with go"
	"""

	def __init__(self):
		self.handlers = set()

	def handle(self, handler):
		"""Attach a hander to the event. Equivalent to ``e += handler``"""
		self.handlers.add(handler)
		return self

	def unhandle(self, handler):
		"""Remove a hander from the event. Equivalent to ``e -= handler``"""
		try:
			self.handlers.remove(handler)
		except:
			raise ValueError("Handler is not handling this event, so cannot unhandle it.")
		return self

	def fire(self, *args, **kargs):
		"""
		Fire the event, triggering all handlers synchronously. Equivalent to
		``e(*args, **kargs)``
		"""
		for handler in self.handlers:
			handler(*args, **kargs)

	@property
	def handlerCount(self):
		return len(self.handlers)

	__iadd__ = handle
	__isub__ = unhandle
	__call__ = fire
	__len__  = handlerCount