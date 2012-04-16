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

import time
import sys
class Profiler(object):
	"""A class for profiling, to be used as a context manager"""
	def __init__(self, name = "Profiler", parent = None):
		"""Create a new profiler, with an optional name"""
		self.parent = parent
		self.name = name
		self.reset()
		self.time = 0
		self.printTo = sys.stdout

	def __enter__(self):
		self.start = time.time()
		return self

	def __exit__(self, t, v, tb):
		self.time = time.time() - self.start

		if self.parent:
			self.parent.times += [self]
		else:
			self.printTimeTree()
		return False

	def event(self, name):
		"""Create a subprofiler, which will time operations within a larger piece of code"""
		return Profiler(name, self)

	def reset(self):
		"""Clear the profiler, so that it can be used again"""
		self.times = []

	def printTimeTree(self, indent = 0):
		"""Print out a tree of timings for events and subevents. Runs when the context is exited"""
		print >> self.printTo, '\t' * indent + '%s: %f' % (self.name, self.time)
		for child in self.times:
			child.printTimeTree(indent+1)

	def __rshift__(self, to):
		"""Redirect output to another stream"""
		self.printTo = to
		return self

def main():
	with Profiler("testing") >> sys.stdout as t:
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