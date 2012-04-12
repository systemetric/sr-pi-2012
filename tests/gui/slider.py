import pygtk
pygtk.require('2.0')
import gtk, gobject, pango
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
	def __init__(self, pidController, max):
		self.pidRange = gtk.Adjustment(
			value = pidController.kp,
			lower = 0,
			upper = max,
			step_incr = max / 200.0
		)
		PIDSlider.__init__(self, pidController)
	def sliderMoved(self, _, adj):
		self.pidController.kp = adj.value

class ISlider(PIDSlider):
	def __init__(self, pidController, max):
		self.pidRange = gtk.Adjustment(
			value = pidController.ki,
			lower = 0,
			upper = max,
			step_incr = max / 200.0
		)
		PIDSlider.__init__(self, pidController)
	def sliderMoved(self, _, adj):
		self.pidController.ki = adj.value
		self.pidController._reset();

class DSlider(PIDSlider):
	def __init__(self, pidController, max):
		self.pidRange = gtk.Adjustment(
			value = pidController.kd,
			lower = 0,
			upper = max,
			step_incr = max / 200.0
		)
		PIDSlider.__init__(self, pidController)
	def sliderMoved(self, _, adj):
		self.pidController.kd = adj.value
		self.pidController._reset();

class SliderWrapper(gtk.HBox):
	def __init__(self, name, slider):
		label = gtk.Label()
		label.set_text_with_mnemonic(name)
		label.set_mnemonic_widget(slider)
		label.show()

		gtk.HBox.__init__(self)

		self.pack_start(label, False, False, 0)
		self.pack_start(slider, True, True, 0)

class PIDWindow(gtk.Window):
	def __init__(self, pidController, max = (5, 20, 0.5)):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
		self.set_border_width(10)
		self.set_title("PID Adjustment")

		pScale = PSlider(pidController, max[0])
		pScale.set_size_request(320, 50)
		pScale.show()
		pControl = SliderWrapper("k_P", pScale)

		iScale = ISlider(pidController, max[1])
		iScale.set_size_request(320, 50)
		iScale.show()
		iControl = SliderWrapper("k_I", iScale)

		dScale = DSlider(pidController, max[2])
		dScale.set_size_request(320, 50)
		dScale.show()
		dControl = SliderWrapper("k_D", dScale)

		errorLabel = gtk.Label("Error")
		errorLabel.show()
		errorValue = gtk.Label("0")
		errorValue.show()
		errorValue.modify_font(pango.FontDescription("sans 48"))

		gobject.timeout_add(100, lambda: errorValue.set_text(str(pidController.error)) or True)


		errorWrapper = gtk.HBox()
		errorWrapper.pack_start(errorLabel, False, False, 0)
		errorWrapper.pack_start(errorValue, True, True, 0)

		pControl.show()
		iControl.show()
		dControl.show()
		errorWrapper.show()

		mainWrapper = gtk.VBox()
		mainWrapper.pack_start(pControl, False, False, 0)
		mainWrapper.pack_start(iControl, False, False, 0)
		mainWrapper.pack_start(dControl, False, False, 0)
		mainWrapper.pack_start(errorWrapper, False, False, 0)
		mainWrapper.show()

		self.add(mainWrapper)
		
		self.show()

	def main(self):
		gtk.gdk.threads_init()
		gtk.main()
	
	def runInBackground(self):
		t = threading.Thread(target=self.main)
		t.start()



