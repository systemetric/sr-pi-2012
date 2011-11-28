import systemetric
import gtk 
import pygtk 

def main():
	R = systemetric.Robot()
	def key_press_event(self, widget, event):
		speed = event.keyval == gtk.keysyms.Up and 100 or
				event.keyval == gtk.keysyms.Down and -100 or
				0

		steer = event.keyval == gtk.keysyms.Left and 50 or
				event.keyval == gtk.keysyms.Right and -50 or
				0

		R.drive(speed = speed, steer = steer)

	w = gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.connect("key_press_event", key_press_event)
	w.show()

	gtk.main()