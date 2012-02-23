import systemetric
import gtk, gobject, cairo
from systemetric.mapping.arenamaps import S007ArenaMap

class Screen(gtk.DrawingArea):
    """ This class is a Drawing Area"""
    def __init__(self):
        super(Screen,self).__init__()
        self.connect("expose_event", self.do_expose_event)
        gobject.timeout_add(50, self.tick)

    def tick(self):
        ## This invalidates the screen, causing the expose event to fire.
        self.alloc = self.get_allocation()
        rect = gtk.gdk.Rectangle(self.alloc.x, self.alloc.y, self.alloc.width, self.alloc.height)
        self.window.invalidate_rect(rect, True)        
        return True # Causes timeout to tick again.

    ## When expose event fires, this is run
    def do_expose_event(self, widget, event):
        self.cr = self.window.cairo_create()
        ## Call our draw function to do stuff.
        self.draw(*self.window.get_size())

class CubeDisplay(Screen):
    def __init__(self):
        super(CubeDisplay, self).__init__()
        self.allTokens = {}
        self.R = systemetric.Robot()
        self.arenaMap = S007ArenaMap()

    def draw(self, w, h):
    	self.width = w
    	self.height = h
    	self.draw_arena(self.cr)

    def draw_robot(self, cr):
        cr.save()
        cr.rectangle(-0.3, -0.3, 0.6, 0.6)
        cr.set_source_rgb(1, 0, 0) 
        cr.fill()

    def draw_arena(self, cr):
    	cr.save()
    	cr.set_line_width(0.05)
        matrix = cairo.Matrix()
        matrix.translate(self.width / 2, self.height / 2)
        matrix.scale(20, 20)
        matrix.translate(-self.size.x / 2, -self.size.y / 2)
        cr.transform(matrix)

    	cr.set_source_rgb(1, 0, 0) 
        for key, marker in self.arenaMap.iteritems():
            cr.move_to(marker.left.x, marker.left.y)
            cr.line_to(marker.right.x, marker.right.y)

        cr.stroke()
        cr.restore()

    def update_pos(self, event=None):
        vision = self.R.see().processed()
        #print markers.tokens
        #print len(markers), markers
        transform = self.arenaMap.estimatePositionFrom(vision)
        if transform:
            for token in vision.tokens:
                #Transform the token to object space
                token.transform(transform)
                #Update it's position
                self.allTokens[token.code] = token
            
            #Print out the location of ALL THE TOKENS
            print [token.center for token in vision.tokens]


def main():
    window = gtk.Window()
    window.connect("delete-event", gtk.main_quit)
    window.set_size_request(400, 400)
    cd = CubeDisplay()
    cd.show()
    window.add(cd)
    window.present()
    gtk.main()