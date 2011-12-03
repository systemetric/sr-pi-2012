import pygtk
pygtk.require('2.0')
import gtk
import threading


class PIDSlider(gtk.HScale):
	def __init__(self, pidController):

		self.pidController = pidController
		gtk.HScale.__init__(self, self.pidRange)
		self.connect("value-changed", self.sliderMoved, self.pidRange)
		self.set_digits(3)
	def sliderMoved(self, _, adj):
		pass

class PSlider(PIDSlider):
	def __init__(self, pidController):
		self.pidRange = gtk.Adjustment(
			value = 0,
			lower = 0,
			upper = 5,
			step_incr = 0.025
		)
		PIDSlider.__init__(self, pidController)
	def sliderMoved(self, _, adj):
		self.pidController.kp = adj.value

class ISlider(PIDSlider):
	def __init__(self, pidController):
		self.pidRange = gtk.Adjustment(
			value = 0,
			lower = 0,
			upper = 5,
			step_incr = 0.025
		)
		PIDSlider.__init__(self, pidController)
	def sliderMoved(self, _, adj):
		self.pidController.ki = adj.value

class DSlider(PIDSlider):
	def __init__(self, pidController):
		self.pidRange = gtk.Adjustment(
			value = 0,
			lower = 0,
			upper = 0.5,
			step_incr = 0.0025
		)
		PIDSlider.__init__(self, pidController)
	def sliderMoved(self, _, adj):
		self.pidController.kd = adj.value

class SliderWrapper(gtk.HBox):
	def __init__(self, name, slider):
		label = gtk.Label(name)
		label.show()

		gtk.HBox.__init__(self)

		self.pack_start(label, False, False, 0)
		self.pack_start(slider, True, True, 0)

class PIDWindow(gtk.Window):
	def __init__(self, pidController):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_border_width(10)
		self.set_title("PID Adjustment")

		pScale = PSlider(pidController)
		pScale.set_size_request(320, 50)
		pScale.show()
		pControl = SliderWrapper("kP", pScale)

		iScale = ISlider(pidController)
		iScale.set_size_request(320, 50)
		iScale.show()
		iControl = SliderWrapper("kI", iScale)

		dScale = DSlider(pidController)
		dScale.set_size_request(320, 50)
		dScale.show()
		dControl = SliderWrapper("kD", dScale)

		pControl.show()
		iControl.show()
		dControl.show()

		mainWrapper = gtk.VBox()
		mainWrapper.pack_start(pControl, False, False, 0)
		mainWrapper.pack_start(iControl, False, False, 0)
		mainWrapper.pack_start(dControl, False, False, 0)
		mainWrapper.show()

		self.add(mainWrapper)

		self.show()

	def main(self):
		gtk.gdk.threads_init()
		gtk.main()
	
	def runInBackground(self):
		t = threading.Thread(target=self.main)
		t.start()



