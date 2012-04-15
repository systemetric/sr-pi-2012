# This file is part of systemetric-student-robotics.

# systemetric-student-robotics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# systemetric-student-robotics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with systemetric-student-robotics.  If not, see <http://www.gnu.org/licenses/>.

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