import systemetric
import gtk
import logs


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
		R.drive(speed, steer)


	def key_press_event(self, event):
		if event.keyval == gtk.keysyms.A:
			R.arm.grabCube(wait = False)
		elif event.keyval == gtk.keysyms.Page_Down:
			R.lifter.up(wait = False)
		elif event.keyval == gtk.keysyms.Page_Up:
			R.lifter.down(wait = False)
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