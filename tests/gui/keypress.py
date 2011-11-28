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