import json
import sys
import inspect
import systemetric

#Load the config file
config = json.load(open('config.json'))
moduleName = config["execute"]

print "Running %s" % moduleName

#Import the module
__import__(moduleName)

#Run its main method
module = sys.modules[moduleName]

if 'main' in dir(module):
	#Is the main method expecting a robot argument?
	if len(inspect.getargspec(module.main).args) > 0:
		#If the module requests a specific type of robot, use it, else use the main one
		R = module.robot() if hasattr(module, 'robot') else systemetric.Robot()
		module.main(R)
	else:
		module.main()
else:
	print "No main method found in %s" % moduleName
