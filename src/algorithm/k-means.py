import sqlite3 as lite
import csv
import sys, os, inspect, logging
import math

from sklearn.cluster import KMeans
from sklearn import datasets

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
  query += " WHERE confidence > 0.85"

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
    if row[0] <= 2303:
      trainingData.append(row[2:])
      trainingDataLabels.append(row[1])

    else:
      testingData.append(row[2:])
      testingDataLabels.append(row[1])

  print "TRAINING", len(trainingData)
  print "TESTING", len(testingData)

def main():
  print "----- IN MAIN -----";
  est = KMeans(n_clusters=6, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)

  est.fit(trainingData)
  print len(est.labels_)

# x = []
# y = []
# with open('abl_data.csv') as csvfile:
# # with open('vxy_data.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#       # x+=[[row['x_relative'],row['y_relative'],row['z_relative']]]
#       # x+=[[row['z_relative']]]
#       # x += [[row['index_z'],row['middle_z'],row['ring_z']]]   ##xvw
#       x += [[row['thumb_z'],row['middle_z']]] ###abl
#       y+=[row['lable']] 

# # print y

# est = KMeans(n_clusters=3)
# est.fit(x)
# print est
# print est.cluster_centers_
# i =0
# # error = 0
# for p in est.labels_:
#   print str(y[i])
#   print p
#   # error+=1
#   i+=1



if __name__ == "__main__":
  # bring in all the data
  loadData('all-data');

  # call the main function
  main();
