import pygtk
pygtk.require('2.0')
import gtk
import threading


class PIDSlider(gtk.HScale):
	def __init__(self):
		pidRange = gtk.Adjustment(
			value = 1,
			lower = 0,
			upper = 5,
			step_incr = 0.1
		)

		gtk.HScale.__init__(self, pidRange)
		self.connect("value-changed", self.sliderMoved, pidRange)

	def sliderMoved(self,_, z):
		print z.value

class PIDWindow:
	def __init__(self):
		

		wrapper = gtk.HBox()

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_border_width(10)
	
		scale = PIDSlider()
		scale.set_size_request(320, 50)
		scale.show()

		label = gtk.Label("kP")
		label.show()

		wrapper.pack_start(label, False, False, 0)
		wrapper.pack_start(scale, True, True, 0)
		wrapper.show()

		self.window.add(wrapper)
		self.window.show()

	def main(self):
		gtk.main()
	

t = threading.Thread(target= PIDWindow().main)	
t.start()



