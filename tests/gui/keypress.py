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

import gtk 
import pygtk 

class KeyGrabbingWindow(Window):
	def __init__(self): 
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL) 
		self.connect("key_press_event", self.key_press_event) 
		self.show() 
		 
	def key_press_event(self, widget, event): 
		if event.keyval == gtk.keysyms.Up: 
			print 'up' 
		elif event.keyval == gtk.keysyms.Down: 
			print 'down'

		if event.keyval == gtk.keysyms.Left: 
			print 'left' 
		elif event.keyval == gtk.keysyms.Right: 
			print 'right'

	def main(self): 
		gtk.main() 
		
gui = KeyGrabbingWindow() 
gui.main()