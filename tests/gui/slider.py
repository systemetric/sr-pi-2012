import pygtk
pygtk.require('2.0')
import gtk
import threading


class PIDSlider(gtk.HScale):
	def __init__(self, pidController):
		pidRange = gtk.Adjustment(
			value = 1,
			lower = 0,
			upper = 5,
			step_incr = 0.025
		)

		self.pidController = pidController
		gtk.HScale.__init__(self, pidRange)
		self.connect("value-changed", self.sliderMoved, pidRange)

	def sliderMoved(self,_, adj):
		self.pidController.kp = adj.value

class PIDWindow(gtk.Window):
	def __init__(self, pidController):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_border_width(10)
		self.set_title("PID Adjustment")

		scale = PIDSlider(pidController)
		scale.set_size_request(320, 50)
		scale.show()

		label = gtk.Label("kP")
		label.show()

		wrapper = gtk.HBox()
		wrapper.pack_start(label, False, False, 0)
		wrapper.pack_start(scale, True, True, 0)
		wrapper.show()

		self.add(wrapper)
		self.show()

	def main(self):
		gtk.gdk.threads_init()
		gtk.main()
	
	def runInBackground(self):
		t = threading.Thread(target=self.main)
		t.start()



