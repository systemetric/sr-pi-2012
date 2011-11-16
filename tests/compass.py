import time
import threading

from systemetric import Robot

class CompassThread(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.R = robot
        self.target = 0
        self.speed = 0
        self.running = True
        
    def run(self):
        while self.running:
            heading = self.R.compass.heading
            error = float(self.target - heading)
            
            self.R.drive(speed = self.speed, steer = error/2)

def main():
    R = SystemetricRobot()
    t = CompassThread(R)
    t.start()
    
    
    t.target = 0
    time.sleep(2.5)
    
    t.speed = 25
    time.sleep(1)
    t.speed = 0
    
    t.target = 90
    time.sleep(2.5)
    
    t.speed = 25
    time.sleep(1)
    t.speed = 0
    
    t.target = 180
    time.sleep(2.5)
    
    t.speed = 25
    time.sleep(1)
    t.speed = 0
    
    t.target = 270
    time.sleep(2.5)
    
    t.speed = 25
    time.sleep(1)
    t.speed = 0
    
    t.target = 0
    t.running = False
    t.join()
    R.stop()