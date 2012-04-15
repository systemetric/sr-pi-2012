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
import gtk
import systemetric.logs as logs


keys = {
	gtk.keysyms.Up: False,
	gtk.keysyms.Down: False,
	gtk.keysyms.Left: False,
	gtk.keysyms.Right: False
}
def main():
	R = systemetric.Robot()
	def update():
		speed = 0
		steer = 0
		if keys[gtk.keysyms.Up]:
			speed +=100
		if keys[gtk.keysyms.Down]:
			speed -= 100
		if keys[gtk.keysyms.Left]:
			steer -= 100
		if keys[gtk.keysyms.Right]:
			steer += 100
		print "Driving"
		R.drive(speed, steer, regulate = False)


	def key_press_event(self, event):
		if event.keyval == gtk.keysyms.A:
			R.arm.grabCube(wait = False)
			print "Grabbed cube!"
		elif event.keyval == gtk.keysyms.Page_Down:
			R.lifter.down(wait = False)
			print "Lifter up!"
		elif event.keyval == gtk.keysyms.Page_Up:
			R.lifter.up(wait = False)
			print "Lifter down!"
		else:
			keys[event.keyval] = True
			update()
	
	def key_release_event(self, event):
		keys[event.keyval] = False
		update()

	w = gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.connect("key_press_event", key_press_event)
	w.connect("key_release_event", key_release_event)
	w.show()

	gtk.main()