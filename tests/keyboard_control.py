import systemetric
import gtk 

def main():
	R = systemetric.Robot()
	def key_press_event(self, event):

		speed = 100 if event.keyval == gtk.keysyms.Up else \
		       -100 if event.keyval == gtk.keysyms.Down else \
		       0

		steer = 50 if event.keyval == gtk.keysyms.Left else \
				- 50 if event.keyval == gtk.keysyms.Right else \
				0
		print speed
		R.drive(speed = speed, steer = steer)

	w = gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.connect("key_press_event", key_press_event)
	w.show()

	gtk.main()