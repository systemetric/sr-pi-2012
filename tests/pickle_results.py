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

import systemetric
import pickle
import time
import os

def main():
	R = systemetric.Robot()
	t = time.strftime("%d %b %Y %H.%M.%S", time.gmtime())
	directory = os.path.join(R.usbkey, t)
	if not os.path.isdir(directory):
		os.mkdir(directory)

	for i in range(20):
		vision = R.see()

		filename = os.path.join(directory, 'visionResult{0}.dat'.format(i))

		with open(filename, 'w') as f:
			pickle.dump(vision, f)
		
		R.power.beep(440, 1)
		time.sleep(5)