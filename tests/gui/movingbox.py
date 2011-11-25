import cairo as C
from math import pi
import gtk

while True:
    for i in xrange(20):        
        def on_expose(widget, event):
            cr = draw.window.cairo_create()
            cr.set_source_rgb(1, 0, 0)
            cr.rectangle(10 + i * 2, 10 + i * 2, 20 + i * 2, 20 + i * 2)
            cr.fill()
        draw = gtk.DrawingArea()
        draw.connect("expose-event", on_expose)
        draw.set_size_request(100,100)
        
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
        window.add(draw)
        window.show_all()
        gtk.main()