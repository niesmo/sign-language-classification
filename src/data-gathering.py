import sys, os, inspect, time
import data.dataCollectionTools
import ConfigParser
import argparse

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

in the args parameter, there are all the arguments that the user passed in from
the command line for this program to run.
'''
def main(args):
  # get the persons information
  getDemographicInformation()

  print "Press Enter when you are ready to start the experiment"
  print "This process will take " + str(args.duration) + " seconds. Keep your hand steady :)"
  sys.stdin.readline()
  
  # get the data collector and start the session
  dataCollector = data.dataCollectionTools.DataCollector.Instance()

  # tell the data collector what letter its collecting
  dataCollector.setDataLabel(args.letter)

  # tell the data collector where to save the data at
  dataCollector.setTargetDatabase(args.db)

  # start collecting data
  dataCollector.start()

  # wait for few seconds
  time.sleep(float(args.duration))

  # Keep this process running until Enter is pressed
  # print "Press Enter to quit..."
  
  # wait for the user to press enter
  # sys.stdin.readline()

  # Stop the data collector which will store the data in the database
  dataCollector.stopAndSave()

def getDemographicInformation():
  print "Getting demographics"
  return


if __name__ == "__main__":
  # getting the arguments from the command line
  parser = argparse.ArgumentParser(description='Data Gathering')
  parser.add_argument('-l', action='store', dest='letter', required=True)
  parser.add_argument('--db', default="data.db", action='store', dest='db')
  parser.add_argument('--duration', default=None, action='store', dest='duration')

  # getting the configs
  dataCollectionDuration = Config.get("data_gathering", "data_collection_duration")

  # getting the arguments from the command line
  args = parser.parse_args()

  if args.duration is None:
    args.duration = dataCollectionDuration

  # print args

  main(args)