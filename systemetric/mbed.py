import serial
from threading import Lock

class MbedDevice(object):
    def __init__(self, id, mbed):
        self.mbed = mbed or Mbed.get()
        self.id = id

    def request(self, thing='', *args):
        command = self.id + thing
        if args:
            command += ','.join(str(r) for r in args)
        
        return self.mbed.sendCommand(command)

class Mbed(object):
    _mainMbed = None
    def __init__(self, port):
        try:
            self.port = serial.Serial(port)
           # self.port.timeout = 0.25
            self.port.open()
            self._lock = Lock()
        except Exception:
            raise Exception('Cannot connect to mbed on %s' % port)


    def sendCommand(self, c):
        with self._lock:
            self.port.write(c)
            return self.port.readline()

    @classmethod
    def get(cls):
        if not cls._mainMbed:
            _mainMbed = cls('/dev/ttyACM0')

        return _mainMbed     
