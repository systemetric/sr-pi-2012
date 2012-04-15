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
from systemetric.mapping.arenamaps import S007ArenaMap

def main():
	R = systemetric.Robot()
	arenaMap = S007ArenaMap()
	while True:
		markers = R.see().processed()
		#print markers.tokens
		#print len(markers), markers
		if markers.arena:
			print arenaMap.estimatePositionFrom(markers)
			#print "==========="
