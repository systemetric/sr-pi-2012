import gtk 
import pygtk 

class keypress(): 
	 
	def __init__(self): 
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL) 
		self.window.connect("key_press_event", self.key_press_event) 
		self.window.show() 
		 
	def key_press_event(self, widget, event): 
		if event.keyval == gtk.keysyms.Up: 
			print 'up' 
		if event.keyval == gtk.keysyms.Down: 
			print 'down'

	def main(self): 
		gtk.main() 
		
gui = keypress() 
gui.main()