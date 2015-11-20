import sqlite3 as lite
import sys, os, inspect, logging, time
import collections
import ConfigParser

from algorithm.clustering import KMeansAlgo
from data.dataCollectionTools import DataCollector

# get the src and other directories
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(curr_dir, '../lib'))
config_file = os.path.abspath(os.path.join(curr_dir, 'config/config.conf'))
db_dir = os.path.abspath(os.path.join(curr_dir, 'data/db'))

import Leap

# setting up the configuration object
Config = ConfigParser.ConfigParser()
Config.read(config_file)

# setting up the global logger
logger = logging.getLogger("Testing Script")

kmean = {}
trainingData = []
trainingDataLabels = []



def loadTrainingData(queryFilename):
  logger.debug("Openning the query file " + queryFilename)

  # getting the config for confidency level
  confidency = Config.get("data_gathering", "confidency_percent")

  # load in the query file
  query = ""
  queryFile = open(db_dir + "/queries/"+ queryFilename +".sql")
  for l in queryFile:
    query += l

  # add the confidence and id in the query
  MAGIC = 4234
  query += " WHERE a.id < " + str(MAGIC) + " AND confidence >" + str(confidency)

  logger.debug("Openning the database connection")

  # query the data base
  connection = lite.connect(db_dir + "/data.db")
  with connection:
    cursor = connection.cursor()

    logger.debug("Executing the query")
    cursor.execute(query)

    rows = cursor.fetchall()
  
  # getting the training data
  for row in rows:  
    trainingData.append(list(row[2:]))
    trainingDataLabels.append(row[1])

  print "Training Data Count: ", len(trainingData)

'''
This function will take in as input an array of inputs and will trun those
info an array that the K-Means test function will take.
Note: the order of the columns in the data will depend on the sql queries
'''
def preProcessTestingData(data):
  preprocessedData = []
  for d in data:

    # if more than one hand, skip
    if len(d.hands) > 1:
      logger.warning("There are more than one hand in the frame. There are", len(self.hands), "hands")
      continue

    selectedHand = d.hands[0]

    # setting up the reference points
    palm_position = selectedHand[Config.get('frame_fields', 'palm_position')]
    palm_direction = selectedHand['direction']

    dataPoint = []

    # adding all the attributes to the data point
    dataPoint.append(selectedHand['sphere_radius']) # sphere radius

    dataPoint.append(palm_direction[0]) # palm position x
    dataPoint.append(palm_direction[1]) # palm position y
    dataPoint.append(palm_direction[2]) # palm position z

    dataPoint.append(palm_direction[0]) # palm direction x
    dataPoint.append(palm_direction[1]) # palm direction y
    dataPoint.append(palm_direction[2]) # palm direction z

    dataPoint.append(selectedHand['normal_direction'][0]) # palm normal direction x
    dataPoint.append(selectedHand['normal_direction'][1]) # palm normal direction y
    dataPoint.append(selectedHand['normal_direction'][2]) # palm normal direction z

    dataPoint.append(selectedHand['wrist_position'][0]) # wrist position x
    dataPoint.append(selectedHand['wrist_position'][1]) # wrist position y
    dataPoint.append(selectedHand['wrist_position'][2]) # wrist position z

    # for all finger indexes
    for fingerIdx in range(Leap.Finger.TYPE_THUMB, Leap.Finger.TYPE_PINKY + 1):
      # tip position
      dataPoint.append(selectedHand['fingers'][fingerIdx][Config.get('frame_fields', 'finger_tip_position')][0] - palm_position[0])
      dataPoint.append(selectedHand['fingers'][fingerIdx][Config.get('frame_fields', 'finger_tip_position')][1] - palm_position[1])
      dataPoint.append(selectedHand['fingers'][fingerIdx][Config.get('frame_fields', 'finger_tip_position')][2] - palm_position[2])

      # metacarpal position
      dataPoint.append(selectedHand['fingers'][fingerIdx]['metacarpal'][0] - palm_position[0])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['metacarpal'][1] - palm_position[1])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['metacarpal'][2] - palm_position[2])

      # proximal position
      dataPoint.append(selectedHand['fingers'][fingerIdx]['proximal'][0] - palm_position[0])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['proximal'][1] - palm_position[1])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['proximal'][2] - palm_position[2])

      # intermediate position
      dataPoint.append(selectedHand['fingers'][fingerIdx]['intermediate'][0] - palm_position[0])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['intermediate'][1] - palm_position[1])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['intermediate'][2] - palm_position[2])

      # distal position
      dataPoint.append(selectedHand['fingers'][fingerIdx]['distal'][0] - palm_position[0])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['distal'][1] - palm_position[1])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['distal'][2] - palm_position[2])

      # finger direction
      dataPoint.append(selectedHand['fingers'][fingerIdx]['direction'][0] - palm_direction[0])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['direction'][1] - palm_direction[1])
      dataPoint.append(selectedHand['fingers'][fingerIdx]['direction'][2] - palm_direction[2])    
      

    # adding the point to the pre processed data array
    preprocessedData.append(dataPoint)
    
  return preprocessedData

def main():
  NUMBER_OF_CLUSTERS = 7
  kmeans = KMeansAlgo(trainingData, trainingDataLabels, NUMBER_OF_CLUSTERS)

  # cluster the training data
  # kmeans.cluster()

  # store the model in the files
  kmeans.retrieveModel()
  # kmeans.storeModel()

  # get the data from leap
  dataCollectionDuration = Config.get("data_gathering", "data_collection_duration")
  dataCollector = DataCollector.Instance()


  print "Press Enter when you are ready to start the experiment"
  print "This process will take " + str(dataCollectionDuration) + " seconds. Keep your hand steady :)"
  sys.stdin.readline()

  # start collecting data
  dataCollector.start()

  # wait for few seconds
  time.sleep(float(dataCollectionDuration))

  # Stop the data collector which will return the data in the buffer
  testingData = dataCollector.stop()
  testingData = preProcessTestingData(testingData)

  # test the data from Leap 
  kmeans.test(testingData)

  # show the report
  kmeans.report()

if __name__ == "__main__":
  # load the training data
  loadTrainingData("all-relative-data")

  # call the main function to get the data from the 
  main()