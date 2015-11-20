from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from sklearn import datasets
from numpy import ravel
import csv
import numpy as np


def loaddata(filename,classes):
	inputDim = None
	#open file and read
	with open (filename, "rb") as csvfile:
		reader = csv.reader(csvfile)
		reader.next() # Skip the header row
		collected = []
		for row in reader:
		    collected.append(list(row))
		# print len(collected[0][2:])
	
	#get inout dimensions
	inputDim=len(collected[0][2:])
	
	#initialize dataset with input dimensions, target dimension and number of classes
	temp = ClassificationDataSet(inputDim, 1, nb_classes=classes)
	
	#add samples from file to the dataset
	for each in collected:
		if each[1] == 'A':
			target = 0
		elif each[1] == "B":
			target = 1
		elif each[1] == "C":
			target = 2
		elif each[1] == 'D':
			target = 3
		elif each[1] == 'E':
			target = 4
		elif each[1] == 'L':
			target = 5	
		elif each[1] == "V":
			target = 6
		elif each[1] == "W":
			target = 7
		elif each[1] == "X":
			target = 8
		elif each[1] == "Y":
			target = 9
		
		temp.addSample(each[2:],target);
		# temp._convertToOneOfMany()
	return temp

def train(filename,classes,hiddenlayers,epochs):
	# load training data
	trndata = ClassificationDataSet(103, 1, nb_classes=classes)
	trndata=loaddata(filename ,classes)
	
	#some sort of mandatory conversion
	trndata._convertToOneOfMany()
	
	#define nerual nets
	net = buildNetwork(103, hiddenlayers[0], hiddenlayers[1], classes, outclass=SoftmaxLayer)
	
	#intialize and define trainer
	trainer = BackpropTrainer(net,dataset=trndata,momentum=0.1,verbose=True,weightdecay=0.01)
	
	#train till convergence
	#trainer.trainUntilConvergence(dataset=trndata,maxEpochs=50)
	
	#train for number of epochs
	trainer.trainOnDataset(trndata,epochs)

	return trainer, net

def test(filename,classes,trainer,net):
	testLabels = []

	#load test data
	tstdata = ClassificationDataSet(103, 1, nb_classes=classes)
	tstdata=loaddata(filename, classes)

	testLabels = tstdata['target'];

	# some sort of mandatory conversion
	tstdata._convertToOneOfMany()
	
	#using numpy array
	output = np.array([net.activate(x) for x, _ in tstdata])
	output = output.argmax(axis=1)
	print(output)
	print("\non test data",percentError( output, tstdata['class'] ))

	for i, l in enumerate(output):
		print l, '->', testLabels[i][0]


	# alternate version - using activateOnDataset function
	out = net.activateOnDataset(tstdata).argmax(axis=1)
	print out
	print("\non test data",percentError( out, tstdata['class'] ))

trainer, net = train("all_data.csv",10,[20,20],150)

test("Test_CE.csv",10,trainer,net)
test("testdata_abl.csv",10,trainer,net)
test("testdata_xvwy.csv",10,trainer,net)


############# Bug fix for if "._convertToOneOfMany()" function throws errors ############

# tstdata = ClassificationDataSet(4, 1, nb_classes=3) 
# for n in xrange(0, tstdata_temp.getLength()):
# 	tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )
# 	# print tstdata.getSample(n)[1]

# trndata = ClassificationDataSet(4, 1, nb_classes=3) 
# for n in xrange(0, trndata_temp.getLength()):
# 	trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

#######################################################################################


