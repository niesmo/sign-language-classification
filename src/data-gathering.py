import sys, os, inspect, time
import data.dataCollectionTools
import ConfigParser


# get the src and other directories
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
config_file = os.path.abspath(os.path.join(curr_dir, 'config/config.conf'))

# setting up the configuration object
Config = ConfigParser.ConfigParser()
Config.read(config_file)

'''
In this script, the user will be prompted to enter the name 
and some information of the person who is making the hand gestures!

And they will be given the choice to start the recording
There will be a timer on the console that shows how much time there is left
At the end, it would show some stats about the data that was recorded -- many the count or the average of the confidence 
'''
def main():
  dataCollectionDuration = Config.get("data_gathering", "data_collection_duration")

  # get the persons information
  getDemographicInformation()

  print "Press Enter when you are ready to start the experiment"
  print "This process will take " + str(dataCollectionDuration) + " seconds. Keep your hand steady :)"
  sys.stdin.readline()

  # get the data collector and start the session
  dataCollector = data.dataCollectionTools.DataCollector.Instance()

  # start collecting data
  dataCollector.start()

  # wait for few seconds
  time.sleep(float(dataCollectionDuration))

  # Keep this process running until Enter is pressed
  # print "Press Enter to quit..."
  
  # wait for the user to press enter
  # sys.stdin.readline()

  # Stop the data collector which will store the data in the database
  dataCollector.stop()

def getDemographicInformation():
  print "Getting demographics"
  return


if __name__ == "__main__":
  main()