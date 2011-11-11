import sys
import math
import os
import serial
from collections import namedtuple

from sr import *
from lib.pyeuclid import *
from lib.twowheeledrobot import TwoWheeledRobot
from lib.compass import Compass

Marker = namedtuple("Marker", "vertices normal location")
Markers = namedtuple("Markers", "tokens robots arena buckets")
Token = namedtuple("Token", "markers id timestamp location")

class SystemetricRobot(TwoWheeledRobot):
    '''A class derived from the base 'Robot' class provided by soton'''     
    def __init__(self):
        #Get the motors set up
        TwoWheeledRobot.__init__(self)
        
        #set up the serial connection to the mbed
        try:
            self.compass = Compass()
        except Exception, c:
            self.end(message = str(c))
        
        #Camera orientation                            
        self.cameraMatrix = Matrix4.new_rotate_euler(    # https://github.com/dov/pyeuclid/blob/master/euclid.txt (line 385)
            heading = 0,                                 # rotation around the y axis
            attitude = -10,                              # rotation around the x axis
            bank = 0                                     # rotation around the z axis
        ) 
        
        #Position and orientation of the robot
        self.robotMatrix = Matrix3()
    
   
    #deprecated
    @property 
    def compassHeading(self):
        return self.compass.heading
    
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
        
    def end(self, message = 'robot stopped', error = True, shutdown = False):
        '''Kill the robot in the nicest way possible'''
        print message
        
        #stop the motors
        self.stop()
        
        #end the program with an exit code
        if shutdown:
            os.system('shutdown -P now')
        else:
            sys.exit(int(error))