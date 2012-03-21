import json
import sys

#Load the config file
config = json.load(open('config.json'))

moduleName = config["execute"]

#Import the module
__import__(moduleName)

#Run its main method
module = sys.modules[moduleName]

if 'main' in dir(module):
	module.main()
else:
	print "No main method found in %s" % moduleName
