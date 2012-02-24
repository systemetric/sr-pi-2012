#import systemetric
import gtk, gobject, cairo, math
from systemetric.mapping.arenamaps import S007ArenaMap
from libs.pyeuclid import *

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
       # self.R = systemetric.Robot()
        self.arenaMap = S007ArenaMap()
        self.tokens = {2: Point2(1, 1), 12: Point2(0.5, 1.75), 0: Point2(3, 1.25)}

    def draw(self, w, h):
        self.cr.save()
        self.initScaling(self.cr, w, h)
    	self.drawArena(self.cr)
        self.drawTokens(self.cr)
        self.cr.restore()

    def drawRobot(self, cr):
        cr.save()
        cr.rectangle(-0.3, -0.3, 0.6, 0.6)
        cr.set_source_rgb(1, 0, 0) 
        cr.fill()

    def initScaling(self, cr, w, h):
        matrix = cairo.Matrix()

        #Move to the middle of the screen
        matrix.translate(w/2, h/2)

        actualWidth, actualHeight = self.arenaMap.size.xy
        scaleFactor = min(w/actualWidth, h/actualHeight)

        #Scale so that a measurement of 1 corresponds to one meter. Flip Y axis to give normal coords
        matrix.scale(scaleFactor, -scaleFactor)

        #Move the middle of the arena to the middle of the screen
        matrix.translate(-actualWidth / 2, -actualHeight / 2)
        cr.transform(matrix)

    def drawArena(self, cr):
    	cr.save()
    	cr.set_line_width(0.01)
    	cr.set_source_rgb(1, 0, 0) 
        for key, marker in self.arenaMap.iteritems():
            cr.move_to(marker.left.x, marker.left.y)
            cr.line_to(marker.right.x, marker.right.y)

        cr.stroke()
        cr.restore()

    def drawTokens(self, cr):
        cr.save()
        cr.set_source_rgb(0, 0, 1)

        for id, token in self.tokens.iteritems():
            cr.arc(token.x, token.y, 0.05, 0.0, 2 * math.pi)
            cr.fill()

        cr.set_source_rgb(1, 1, 1)
        cr.set_font_size(0.1)
        m = cairo.Matrix()
        m.scale(1, -1)
        cr.transform(m)
        for id, token in self.tokens.iteritems():
            cr.move_to(token.x, token.y)
            cr.show_text(str(id))

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