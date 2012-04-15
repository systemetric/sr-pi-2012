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

import json
import sys
import inspect
import systemetric

#Load the config file
config = json.load(open('config.json'))
moduleName = config["execute"]

print "Running %s" % moduleName

#Import the module
__import__(moduleName)

#Run its main method
module = sys.modules[moduleName]

if 'main' in dir(module):
	#Is the main method expecting a robot argument?
	if len(inspect.getargspec(module.main).args) > 0:
		#If the module requests a specific type of robot, use it, else use the main one
		R = module.robot() if hasattr(module, 'robot') else systemetric.Robot()
		print 'Battery Voltage: %.2f' % R.power.battery.voltage
		print 'Competition mode: %s' % R.mode
		module.main(R)
	else:
		module.main()
else:
	print "No main method found in %s" % moduleName
