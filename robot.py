import json

#Load the config file
config = json.load(open('config.json'))

module = config["execute"]

#Import the module
__import__(module)

#Run its main method
sys.modules[module].main()
