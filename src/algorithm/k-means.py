import sqlite3 as lite
import csv
import sys, os, inspect, logging
import math, collections

from sklearn.cluster import KMeans
from sklearn import datasets
# TESTING
from sklearn.datasets import load_digits
from sklearn.preprocessing import scale

curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
db_file = os.path.abspath(os.path.join(curr_dir, '../data/db/data.db'))

testingData = []
testingDataLabels = []

trainingData = []
trainingDataLabels = []

def loadData(queryFilename):
  # load in the query file
  query = ""
  queryFile = open("../data/db/queries/"+ queryFilename +".sql")
  for l in queryFile:
    query += l

  
  # add the confidence in the query
  # WARNING: if you change this, you have to change the MAGIC number
  query += " WHERE confidence > 0.85"
  magic = 2303

  # query the data base
  connection = lite.connect(db_file)
  with connection:
    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
  
  # define the training and testing data
  # training <= 2309 Testing >= 2526
  for row in rows:
    # MAGIC NUMBER -> Change when needed
    if row[0] <= magic:
      trainingData.append(list(row[2:]))
      trainingDataLabels.append(row[1])

    else:
      testingData.append(list(row[2:]))
      testingDataLabels.append(row[1])

  print "TRAINING", len(trainingData)
  print "TESTING", len(testingData)

def preProcess():
  pass

def main():
  kmeans = KMeans(n_clusters=6, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
  kmeans.fit(trainingData, trainingDataLabels)


  print "\n\nDistribution of Training Results"; print 50 * '-'
  counter=collections.Counter(kmeans.labels_)
  print counter

  # I had to hard code these values, I havent found a way to give the scipy all the labels
  labels = {
    0: 'L',
    2: 'V',
    3: 'Y',
    4: 'W',
  }

  print "\n\nDistribution of Test Data"; print 50 * '-'
  counter=collections.Counter(testingDataLabels)
  print counter
  
  testResults = kmeans.predict(testingData)

  print "\n\Test Results after running k-means"; print 50 * '-'
  counter=collections.Counter(testResults)
  print counter

  for i, d in enumerate(testResults[:10]):
    print d, testingDataLabels[i]


if __name__ == "__main__":
  # bring in all the data
  loadData('all-relative-data')

  # pre process the data
  preProcess()

  # call the main function
  main()