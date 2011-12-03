import pygtk
pygtk.require('2.0')
import gtk
import threading


class PIDSlider(gtk.HScale):
	def __init__(self, pidController):
		pidRange = gtk.Adjustment(
			value = 2.45,
			lower = 0,
			upper = 5,
			step_incr = 0.025
		)

		self.pidController = pidController
		gtk.HScale.__init__(self, pidRange)
		self.connect("value-changed", self.sliderMoved, pidRange)
		self.set_digits(3)
	def sliderMoved(self, _, adj):
		pass

	class PSlider(PIDSlider):
		def sliderMoved(self, _, adj):
			self.pidController.kp = adj.value
	class ISlider(PIDSlider):
		def sliderMoved(self, _, adj):
			self.pidController.ki = adj.value
	class DSlider(PIDSlider):
		def sliderMoved(self, _, adj):
			self.pidController.kd = adj.value

class PIDWindow(gtk.Window):
	def __init__(self, pidController):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_border_width(10)
		self.set_title("PID Adjustment")

		pScale = PIDSlider.PSlider(pidController)
		pScale.set_size_request(320, 50)
		pScale.show()

		pLabel = gtk.Label("kP")
		pLabel.show()

		pWrapper = gtk.HBox()
		pWrapper.pack_start(pLabel, False, False, 0)
		pWrapper.pack_start(pScale, True, True, 0)
		pWrapper.show()

		dScale = PIDSlider.Dslider(pidController)
		dScale.set_size_request(320, 50)
		dScale.show()
		
		dLabel = gtk.Label("kD")
		dLabel.show()

		dWrapper = gtk.HBox()
		dWrapper.pack_start(dLabel, False, False, 0)
		dWrapper.pack_start(dScale, True, True, 0)
		dWrapper.show()

		self.add(pWrapper)
		self.add(dWrapper)

		self.show()

	def main(self):
		gtk.gdk.threads_init()
		gtk.main()
	
	def runInBackground(self):
		t = threading.Thread(target=self.main)
		t.start()



