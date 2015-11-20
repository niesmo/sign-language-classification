import sqlite3 as lite
import csv
import sys, os, inspect, logging
import math, collections, numpy

from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.decomposition import PCA

NUMBER_OF_CLUSTERS = 7
CONFIDENCY_PERCENT = 0.0

curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
db_file = os.path.abspath(os.path.join(curr_dir, '../data/db/data.db'))

# global data files
testingData = []
testingDataLabels = []

trainingData = []
trainingDataLabels = []

# these are the points that we use to find the labels for each cluster
knownPoints = {}

# defining the logger
logger = logging.getLogger("K-Means Algorithm")

def loadData(queryFilename):
  logger.debug("Openning the query file " + queryFilename)

  # load in the query file
  query = ""
  queryFile = open("../data/db/queries/"+ queryFilename +".sql")
  for l in queryFile:
    query += l

  
  # add the confidence in the query
  # WARNING: if you change this, you have to change the MAGIC number
  query += " WHERE confidence >" + str(CONFIDENCY_PERCENT)
  magic = 3175


  logger.debug("Openning the database connection")
  # query the data base
  connection = lite.connect(db_file)
  with connection:
    cursor = connection.cursor()

    logger.debug("Executing the query")
    cursor.execute(query)

    rows = cursor.fetchall()
  
  # define the training and testing data
  # training <= 2309 Testing >= 2526
  for row in rows:
    # MAGIC NUMBER -> Change when needed
    if row[0] <= magic:
      trainingData.append(list(row[2:]))
      trainingDataLabels.append(row[1])

      if not knownPoints.has_key(row[1]):
        knownPoints[row[1]] = numpy.array(row[2:])

    else:
      testingData.append(list(row[2:]))
      testingDataLabels.append(row[1])

  print "TRAINING", len(trainingData)
  print "TESTING", len(testingData)

  for label in knownPoints:
    print label, knownPoints[label][:2]

def preProcess():
  logger.info("pre-processing the data ...")
  return

def main():
  logger.info("main function: defining the k-means estimator")
  kmeans = KMeans(n_clusters=NUMBER_OF_CLUSTERS, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)

  # PCA 
  

  logger.info("Running k-means for " + str(len(trainingData)) + " data points")
  kmeans.fit(trainingData)
  logger.info("Finished running k-means")

  # finding what cluster are what labels
  # TODO: put this in a function
  labelToLetterMap = {}

  for p in knownPoints:
    m_min = 10000000;
    for i, cluster in enumerate(kmeans.cluster_centers_):
      dist = numpy.linalg.norm(cluster - knownPoints[p])
      if dist < m_min:
        m_min = dist
        labelToLetterMap[p] = i

  print "\n\nLabel to letter mapping:"
  print labelToLetterMap


  print "\n\nDistribution of Training labels"; print 50 * '-'
  counter=collections.Counter(kmeans.labels_)
  print counter

  print "\n\nDistribution of Test Data"; print 50 * '-'
  counter=collections.Counter(testingDataLabels)
  print counter
  
  testResults = kmeans.predict(testingData)

  print "\n\nTest Results after running k-means"; print 50 * '-'
  counter=collections.Counter(testResults)
  print counter



if __name__ == "__main__":
  # bring in all the data
  loadData('all-relative-data')

  # pre process the data
  preProcess()

  # call the main function
  main()