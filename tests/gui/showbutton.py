import pygtk
pygtk.require('2.0')
import gtk

class HelloWorld:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(10)
        self.button = gtk.Button("Hello World")
        self.window.add(self.button)
    
        self.button.show()
    
        self.window.show()

    def main(self):
        gtk.main()
        
hello = HelloWorld()
hello.main()