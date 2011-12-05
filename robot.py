import json

#Load the config file
config = json.load('config.json')

#Import the module
__import__(config.execute)

#Run its main method
sys.modules[config.execute].main()
