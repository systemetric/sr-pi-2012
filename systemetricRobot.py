import sys, math, serial
from collections import namedtuple

from sr import *
from lib.pyeuclid import *

Marker = namedtuple("Marker", "vertices normal location")
Markers = namedtuple("Markers", "tokens robots arena buckets")
Token = namedtuple("Token", "markers id timestamp location")

class SystemetricRobot(Robot):
    '''A class derived from the base 'Robot' class provided by soton'''     
    def __init__(self):
        #Make sure the soton class is initiated, so we can connect to motors
        Robot.__init__(self)
        
        #Name the motors, for easy access
        self.leftMotor = self.motors[0]
        self.rightMotor = self.motors[1]
        
        #set up the serial connection to the mbed
        try:
            self.port = serial.Serial('/dev/ttyACM0')
            self.port.timeout = 0.25
            self.port.open()
        except Exception, c:
            #kill the robot on an error
            self.end(message = str(c) + ' - mbed not connectable')
            
        
        #Camera orientation                            
        self.cameraMatrix = Matrix4.new_rotate_euler(    #https://github.com/dov/pyeuclid/blob/master/euclid.txt (line 385)
            heading = 0,                                 #rotation around the y axis
            attitude = -10,                              #rotation around the x axis
            bank = 0                                     #rotation around the z axis
        )
        
        #Position and orientation of the robot
        self.robotMatrix = Matrix3()
    
    #Getters and setters for left motor. Allows you to write R.left = 100 for full speed forward
    @property
    def left(self):
        '''Property to control the speed of the left motor, without the hassle of `.target`'''
        return self.leftMotor.target
        
    @left.setter
    def left(self, value):
        if not math.isnan(value):
            self.leftMotor.target = value
        
    @property  
    def right(self):
        '''Property to control the speed of the right motor, without the hassle of `.target`'''
        return self.rightMotor.target
        
    @right.setter    
    def right(self, value):
        if not math.isnan(value):
            self.rightMotor.target = value
    
    def stop(self):
        '''Stop the robot, by setting the speed of both motors to 0'''
        self.right = 0
        self.left = 0
        
    def drive(self, speed=50, steer=0):
        '''Drive the robot forwards or backwards at a certain speed, with an optional steer'''
        self.right = speed - steer
        self.left = speed + steer
        
    def turn(self, speed):
        '''Rotate the robot at a certain speed. Positive is clockwise'''
        self.right = -speed
        self.left = speed
    
    @property 
    def compassHeading(self):
        '''Get the compass heading from the mbed'''
        self.port.write('H')
        heading = self.port.readline()
        if heading:
            return int(heading) / 10.0 #convert the int we get from the mbed into a float.
        else:
            return float('nan') #return NaN, because we don't know the heading
    
    def getMarkersById(self):
        '''Get all the markers, grouped by id.
        For example, to get the token with id 1, use:
        
            markers = R.getMarkersById()
            
            # Check if token 0 is visible
            if 0 in marker.tokens:
                markersOnFirstToken = markers.tokens[0]
        '''
        markers = self.see()
        markersById = Markers(tokens={}, arena={}, robots={}, buckets={})
        
        for marker in markers:
            id = marker.info.offset
            type = marker.info.markerType
            
            # What type of marker is it?
            if type == MARKER_TOKEN:
                list = markersById.tokens
            elif type == MARKER_ARENA:
                list = markersById.arena
            elif type == MARKER_ROBOT:
                list = markersById.robots
            else:
                list = markersById.buckets
            
            #Is this the first marker we've seen for this object?
            if not id in list:
                list[id] = []
                
            #Add this marker to the list of markers for this object
            list[id].append(marker)
        
        return markers
    
    def visibleCubes(self):
        markersById = self.getMarkersById()
        
        tokens = []
        # For each token
        for markerId, markers in markersById.tokens.iteritems():
            newmarkers = []
            # Convert all the markers to a nicer format, using pyeuclid
            for marker in markers:
            
                vertices = []
                # We only care about 3D coordinates - keep those
                for v in marker.vertices:
                    vertices.append(Point3(
                        v.world.x,
                        v.world.y,
                        v.world.z
                    ))
                
                # Calculate the normal vector of the surface
                edge1 = vertices[0] - vertices[1]
                edge2 = vertices[2] - vertices[1]
                normal = edge1.cross(edge2).normalize()
                
                # Keep the center position
                location = marker.center.world

                newmarkers.append(Marker(
                    location = Point3(location.x, location.y, location.z),
                    normal = normal,
                    vertices = vertices
                ))
            
            token = Token(
                markers = newmarkers,
                timestamp = marker[0].timestamp,
                id = markerId,
                location = self.cameraMatrix * newmarkers[0].center
            )
            # Take into account the position of the robot
            # token.location = self.robotMatrix * token.Location
            tokens.append(token)
        
        #sort by distance, for convenience
        tokens.sort(key=lambda m: m.location.magnitude())
        return tokens
        
    def end(self, message = 'robot stopped', error = True):
        '''Kill the robot in the nicest way possible'''
        print message
        
        #stop the motors
        self.stop()
        
        #end the program with an exit code
        sys.exit(int(exit))