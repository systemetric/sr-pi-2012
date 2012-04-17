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

import serial
from threading import Lock

class MbedDevice(object):
	"""
	A device attached to an mbed. The protocol is to send a single character
	representing the device ID, then another (if necessary) to specify what
	information should be retrieved. Arguments can be given in a function-
	like syntax. For example:::

		MbedDevice('G').request('r', 10) -> Gr(10)
		MbedDevice('C').request('h')      -> Ch

	The mbed then returns a single line response. The line may be empty
	"""
	def __init__(self, id, mbed=None):
		"""Construct a device with a given id"""
		self.mbed = mbed or Mbed.get()
		self.id = id

	def request(self, thing='', *args):
		"""Request something from the mbed"""
		command = self.id + thing
		if args:
			command += '(' + ','.join(str(r) for r in args) + ')'
		
		return self.mbed.sendCommand(command)

class Mbed(object):
	"""The mbed itself, and basic communications with it"""
	def __init__(self, port):
		try:
			self.port = serial.Serial(port)
			# self.port.timeout = 0.25
			self.port.open()
			self._lock = Lock()
		except Exception:
			raise Exception('Cannot connect to mbed on %s' % port)


	def sendCommand(self, c):
		"""
		Send a short command, and return a single line response. Prevents other
		threads interweaving requests by locking on self._lock
		"""
		with self._lock:
			self.port.flushInput()
			self.port.write(c)
			return self.port.readline()

	_mainMbed = None

	@classmethod
	def get(cls):
		"""
		A lazy singleton, using the default port. This should be used instead
		of calling the constructor, to prevent the serial port being opened
		twice
		"""
		if not cls._mainMbed:
			_mainMbed = cls('/dev/ttyACM0')

		return _mainMbed     
