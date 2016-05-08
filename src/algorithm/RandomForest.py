from sklearn.ensemble import RandomForestClassifier
import os, inspect
import csv
import numpy as np
import pickle

class RandomForest:
	curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
	trainedModelsDir = os.path.abspath(os.path.join(curr_dir, '../trainedModels/RF'))

	def load_training_data(self):
		attributes = []
		labels = []

		#open file and read
		with open ("train_all.csv", "rb") as csvfile:
			reader = csv.reader(csvfile)
			reader.next() # Skip the header row
			for row in reader:
			    attributes.append(row[3:])
			    labels.append(row[1])

		print len(attributes[0]),len(attributes)
		print len(labels[0]),len(labels)

		return np.asarray(attributes).astype(np.float),np.asarray(labels)

	def load_testing_data(self):
		attributes = []
		labels = []

		#open file and read
		with open ("test_all.csv","rb") as csvfile:
			reader = csv.reader(csvfile)
			reader.next() # Skip the header row
			for row in reader:
			    attributes.append(row[3:])
			    labels.append(row[1])

		print len(attributes[0]),len(attributes)
		print len(labels[0]),len(labels)

		return np.asarray(attributes).astype(np.float),np.asarray(labels)

	def pickleModel(self,classifier):	
		# opening the files for the pickles
		pickleFile = open(self.trainedModelsDir+'/RFclassifier.pkl', 'wb')

		#pickleit
		pickle.dump(classifier, pickleFile)

		# closing the files
		pickleFile.close()
		return

	def unpickleModel(self):
		# opening the files for the pickles
		pickleFile = open(self.trainedModelsDir+'/RFclassifier.pkl', 'rb')

		#Unpickling
		classifier = pickle.load(pickleFile)

		# closing the files
		pickleFile.close()

		return classifier

	def train(self):
		X_train, labels_train = self.load_training_data()
		X_test, labels_test = self.load_testing_data()
		clf = RandomForestClassifier(n_estimators=25)
		clf = clf.fit(X_train,labels_train)
		self.pickleModel(clf)

	def livetest(self,data):
		clf = self.unpickleModel()
		print "\nRF - ",clf.predict(np.asarray(data))[0]
		return clf.predict(np.asarray(data))[0]

# RandomForest().train()