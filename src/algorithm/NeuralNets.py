from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from sklearn import datasets
from numpy import ravel
import csv
import numpy as np
import matplotlib.pyplot as pl
import pickle
import os,inspect

class NeuralNets:
	def __init__(self):
		self.curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
		self.trainedModelsNNDir = os.path.abspath(os.path.join(self.curr_dir, '../trainedModels/NN'))
		self.labelToLetter = {
			'0':'A',
			'1':'B',
			'2':'C',
			'3':'E',
			'4':'L',
			'5':'V',
			'6':'W',
			'7':'X',
			'8':'Y'
		}
		return

	def loaddata(self,filename,classes):
		inputDim = None
		#open file and read
		with open (filename, "rb") as csvfile:
			reader = csv.reader(csvfile)
			reader.next() # Skip the header row
			collected = []
			for row in reader:
			    collected.append(list(row))
			# print len(collected[0][2:])
		
		#get input dimensions
		inputDim=len(collected[0][3:])
		
		#initialize dataset with input dimensions, target dimension and number of classes
		temp = ClassificationDataSet(inputDim, 1, nb_classes=classes)
		
		#add samples from file to the dataset
		for each in collected:
			if each[1] == "A":
			  target = 0
			elif each[1] == "B":
			  target = 1
			elif each[1] == "C":
			  target = 2
			elif each[1] == "E":
			  target = 3
			elif each[1] == "L":
			  target = 4
			elif each[1] == "V":
			  target = 5
			elif each[1] == "W":
			  target = 6
			elif each[1] == "X":
			  target = 7
			elif each[1] == "Y":
			  target = 8
			else:
			  target = 9
			temp.addSample(each[3:],target);
			# temp._convertToOneOfMany()
		return temp

	def train(self,filename,classes,hiddenlayers,epochs):
		# load training data
		trndata = ClassificationDataSet(103, 1, nb_classes=classes)
		trndata = self.loaddata(filename,classes)
		
		print len(trndata['target']),len(trndata['input'])
		#some sort of mandatory conversion
		trndata._convertToOneOfMany()
		
		#define nerual nets
		net = buildNetwork(103,hiddenlayers[0],hiddenlayers[1],classes,outclass=SoftmaxLayer)
		
		#intialize and define trainer
		trainer = BackpropTrainer(net,dataset=trndata,momentum=0.1,verbose=True,weightdecay=0.01)
		
		# train till convergence
		trainer.trainUntilConvergence(dataset=trndata,maxEpochs=150)
		print "trained till convergence", trainer.totalepochs

		# # train for number of epochs
		# trainer.trainOnDataset(trndata,epochs)
		
		return trainer, net

	def test(self,filename,classes,trainer,net):
		testLabels = []

		#load test data
		tstdata = ClassificationDataSet(103, 1, nb_classes=classes)
		tstdata = self.loaddata(filename, classes)

		testLabels = tstdata['target'];

		# some sort of mandatory conversion
		tstdata._convertToOneOfMany()
		
		# using numpy array
		output = np.array([net.activate(x) for x, _ in tstdata])
		output = output.argmax(axis=1)
		print(output)
		print("on test data",percentError( output, tstdata['class'] ))

		for i, l in enumerate(output):
			print l, '->', testLabels[i][0]

		# alternate version - using activateOnDataset function
		out = net.activateOnDataset(tstdata).argmax(axis=1)
		print out
		return percentError( out, tstdata['class'])

	def livetest(self,data):
		trainer, net = self.unpickleModel()
		testData = ClassificationDataSet(103, 1, nb_classes=9)
		testData.addSample(data[0],1);
		testData._convertToOneOfMany()
		out = net.activateOnDataset(testData).argmax(axis=1)
		percentError(out, testData['class'])
		print self.labelToLetter[str(out[0])]
		return self.labelToLetter[str(out[0])]

	def pickleModel(self,trainer,net):
		
		# opening the files for the pickles
		pickleFileNNtrainer = open(self.trainedModelsNNDir+'/NNtrainerconvg.pkl', 'wb')
		pickleFileNNnet = open(self.trainedModelsNNDir+'/NNnetconvg.pkl', 'wb')

		#pickleit
		pickle.dump(trainer, pickleFileNNtrainer)
		pickle.dump(net, pickleFileNNnet)

		# closing the files
		pickleFileNNtrainer.close()
		pickleFileNNnet.close()
		return

	def unpickleModel(self):
		# opening the files for the pickles
		pickleFileNNtrainer = open(self.trainedModelsNNDir + '/NNtrainerconvg.pkl', 'rb')
		pickleFileNNnet = open(self.trainedModelsNNDir + '/NNnetconvg.pkl', 'rb')

		#Unpickling
		trainer = pickle.load(pickleFileNNtrainer)
		net = pickle.load(pickleFileNNnet)

		# closing the files
		pickleFileNNtrainer.close()
		pickleFileNNnet.close()

		return trainer, net

def trainModel():
	nn = NeuralNets()
	trainer, net = nn.train("train_all.csv",9,[50,50],1)
	nn.test("test_all.csv",9,trainer,net)
	nn.pickleModel(trainer,net)
	return

if __name__ == "__main__":
	trainModel()



############# Bug fix for if "._convertToOneOfMany()" function throws errors ############

# tstdata = ClassificationDataSet(4, 1, nb_classes=3) 
# for n in xrange(0, tstdata_temp.getLength()):
# 	tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )
# 	# print tstdata.getSample(n)[1]

# trndata = ClassificationDataSet(4, 1, nb_classes=3) 
# for n in xrange(0, trndata_temp.getLength()):
# 	trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

#######################################################################################


