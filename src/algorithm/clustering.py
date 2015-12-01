import sys, os, inspect, logging, pickle
import collections, numpy

from sklearn.cluster import KMeans
# from sklearn import datasets

class KMeansAlgo:
  def __init__(self, data=[], labels=[], clusterCount=0):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.debug("Initializing")

    self.clusterCount = clusterCount
    self.trainingData = data
    self.trainingDataLabels = labels
    self.testingData = []

    # initializing the k-means algorithm
    self.kmeans = KMeans(n_clusters=self.clusterCount, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=8)
    self.letterToLabelMap = {}
    self.results = []

    # pre process the data
    self.preProcess()
    
  def cluster(self):
    self.logger.info("Starting clustering the data using K-Means")

    # find the mapping between clusters and labels
    mappingIsDistinct = True
    
    while mappingIsDistinct:
      tempDict = {}

      self.kmeans.fit(self.trainingData)
      self.mapLabelsToLetters()

      for letter in self.letterToLabelMap:
        label = self.letterToLabelMap[letter]

        if not tempDict.has_key(label):
          tempDict[label] = True
        else:
          mappingIsDistinct = False
          break;

      mappingIsDistinct = not mappingIsDistinct

  def mapLabelsToLetters(self):
    knownPoints = {}

    self.logger.debug("Getting known points for each label")
    # get known points for each letter
    counter = 0
    for i, d in enumerate(self.trainingData):
      if not knownPoints.has_key(self.trainingDataLabels[i]):
        knownPoints[self.trainingDataLabels[i]] = numpy.array(d)
        counter += 1

        # if we have a known point for every cluster, move on
        if counter == self.clusterCount:
          break;


    self.logger.debug("Mapping cluster to labels using the known points")
    # map those letter using the cluster
    for p in knownPoints:
      m_min = sys.maxint;
      for i, cluster in enumerate(self.kmeans.cluster_centers_):
        dist = numpy.linalg.norm(cluster - knownPoints[p])
        if dist < m_min:
          m_min = dist
          self.letterToLabelMap[str(p)] = i

  def test(self, data):
    self.logger.info("Starting to predict the data")

    self.testingData = data
    self.results = self.kmeans.predict(self.testingData)

    return self.results

  def report(self, verbose=True):
    # print self.letterToLabelMap
    resultFrequency = collections.Counter(self.results)

    if verbose:
      print "MAP: ", self.letterToLabelMap

    for letter in self.letterToLabelMap:
      label = self.letterToLabelMap[letter]
      if resultFrequency.has_key(label) and verbose:
        print letter + " -> " + str(resultFrequency[label] * 100 / float(len(self.testingData))) + "%"

    if verbose:
      print resultFrequency

    return resultFrequency

  def preProcess(self):
    self.logger.debug("Pre-processing the data")
    return

  ''' 
  This function will store the k-means object in a file and later will store it
  in the `trainedModels/k-means` directory
  '''
  def storeModel(self):
    curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    trainedModelsKmeansDir = os.path.abspath(os.path.join(curr_dir, '../trainedModels/K-Means'))


    # opening the files for the pickles
    pickleFileKmeans = open(trainedModelsKmeansDir + '/kmeans.pkl', 'wb')
    pickleFileLetterToLabel = open(trainedModelsKmeansDir + '/letterToLabel.pkl', 'wb')
        
    #pickleit
    pickle.dump(self.kmeans, pickleFileKmeans)
    pickle.dump(self.letterToLabelMap, pickleFileLetterToLabel)
    
    # closing the files
    pickleFileKmeans.close()
    pickleFileLetterToLabel.close()
  
  '''
  This function will get the k-means object from the file and will return
  '''
  def retrieveModel(self):
    curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    trainedModelsKmeansDir = os.path.abspath(os.path.join(curr_dir, '../trainedModels/K-Means'))

    # opening the files for the pickles
    pickleFileKmeans = open(trainedModelsKmeansDir + '/kmeans.pkl', 'rb')
    pickleFileLetterToLabel = open(trainedModelsKmeansDir + '/letterToLabel.pkl', 'rb')

    self.kmeans = pickle.load(pickleFileKmeans)
    self.letterToLabelMap = pickle.load(pickleFileLetterToLabel)
  
