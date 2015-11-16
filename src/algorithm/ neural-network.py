from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pylab import ion, ioff, figure, draw, contourf, clf, show, hold, plot
from scipy import diag, arange, meshgrid, where
from numpy.random import multivariate_normal
import sys, os, inspect, logging
import collections, numpy
import sqlite3 as lite
import csv
import sys, os, inspect, logging
import math, collections, numpy



# means = [(-1,0),(2,4),(3,1)]
# cov = [diag([1,1]), diag([0.5,1.2]), diag([1.5,0.7])]
# alldata = ClassificationDataSet(2, 1, nb_classes=3 ,class_labels=['Fish','Chips','lele'])
# for n in xrange(400):
#     for klass in range(3):
#         input = multivariate_normal(means[klass],cov[klass])
#         alldata.addSample(input, [klass])

# print alldata._convertToOneOfMany( )

# print alldata['input'][0], alldata['target'][0], alldata['class'][3]

NUMBER_OF_CLUSTERS = 7
CONFIDENCY_PERCENT = 0.0

curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
db_file = os.path.abspath(os.path.join(curr_dir, '../data/db/data.db'))

# global data files
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
  query += " WHERE confidence >" + str(CONFIDENCY_PERCENT)
  magic = 3175


  # logger.debug("Openning the database connection")
  # query the data base
  connection = lite.connect(db_file)
  with connection:
    cursor = connection.cursor()

    # logger.debug("Executing the query")
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

  print "TRAINING", len(trainingData[0])
  print "TESTING", len(testingData)


def preProcess():
  # logger.info("pre-processing the data ...")
  return

def main():
	label_map = {'A':0,'B':1,'L':2,'X':3,'V':4,'Y':5,'W':6}
	class_map = {0:'A',1:'B',2:'L',3:'X',4:'V',5:'Y',6:'W'}
 	alldata = ClassificationDataSet(103, nb_classes=7 ,class_labels=['A','B','L','X','V','Y','W'])
 	testdata = ClassificationDataSet(103, nb_classes=7 ,class_labels=['A','B','L','X','V','Y','W'])
 	print len(trainingData)
 	print alldata.outdim
 	for i,data in enumerate(trainingData):
 		alldata.addSample(data, label_map[trainingDataLabels[i]])

 	for i,data in enumerate(testingData):
 		testdata.addSample(data, label_map[testingDataLabels[i]])
 	
 	alldata._convertToOneOfMany()
 	testdata._convertToOneOfMany()
 	fnn = buildNetwork( alldata.indim, 10,7, outclass=SoftmaxLayer ) 	
 	trainer = BackpropTrainer( fnn, dataset=alldata, momentum=0.1, verbose=True, weightdecay=0.01)
 	trainer.trainUntilConvergence(dataset = alldata, maxEpochs=100, continueEpochs=10, verbose=True)
 	# trainer.trainEpochs( 5 )
 	# trainer.trainOnDataset(alldata,100)
 	print trainer.totalepochs
 	trnresult = percentError( trainer.testOnClassData(),alldata['class'] )
 	tstresult = percentError( trainer.testOnClassData( dataset=testdata ), testdata['class'] )
 	print "epoch: %4d" % trainer.totalepochs, \
  "  train error: %5.2f%%" % trnresult, \
  "  test error: %5.2f%%" % tstresult
	out = fnn.activateOnDataset(testdata)
	out = out.argmax(axis=1)
	# for i,o in enumerate(out):
	# 	print testingDataLabels[i]
	# 	print class_map[o]



if __name__ == "__main__":
  # bring in all the data
  loadData('all-relative-data')

  # pre process the data
  preProcess()

  # call the main function
  main()