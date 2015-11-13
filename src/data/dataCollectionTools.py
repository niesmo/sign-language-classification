import sys, os, inspect, thread, time, logging
import listeners.dataCollectorListener as dcl

# get the src and lib directories
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(curr_dir, '../../lib/leap'))

# including the lib folder to be able to import the lib dir
sys.path.insert(0, lib_dir)

import Leap
import util.singleton as utilily

from progressbar import Bar, Percentage, ProgressBar


@utilily.Singleton
class DataCollector:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.debug("Initializing")

    self.data = []
    self.label = ""
    self.controller = None
    self.listener = None


  '''
  This function really just attach the controller and starts collecting data into an array
  '''
  def start(self):
    self.logger.info("Started Collecting Data")

    # create a listener of time Data Collector
    self.listener = dcl.DataCollectorListener()

    # https://developer.leapmotion.com/documentation/python/api/Leap.Controller.html#Leap.Controller
    self.controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    self.controller.add_listener(self.listener)
    

  '''
  This function will stop the data collector
  this function will also retruns all the data in the buffer
  '''
  def stop(self):
    self.logger.info("Stopping the Data Collection, removing the Listener, and starting to insert the data to DB")
    # removing the data collection listener
    self.controller.remove_listener(self.listener)

    self.logger.info("length of the data is: " + str(len(self.data)))

    return self.data


  '''
  This function will stop the data collector and will store the data in the database
  The buffer of the Listener is also cleared by the end of this function
  '''
  def stopAndSave(self):
    self.stop();

    # setting the progress bar
    pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(self.data)).start()

    # saving the rows
    for i,frame in enumerate(self.data):
      # save the frame in the data base
      frame.save(self.label)

      # update the progress bar
      pbar.update(i)

    # clearing the buffer
    self.clearData()

  """
  This function adds the frame passed into the method
  to the data property of this class
  """
  def addFrame(self, frame):
    self.logger.debug("Frame added to the data")

    # add the frame to the data property
    self.data.append(frame)

  """
  This function will erase the whole data array and 
  initialize the data with a new empty array
  """
  def clearData(self):
    self.logger.debug("The data of the data collector is being cleared")

    del self.data[:]
    self.data = []

  def setDataLabel(self, letter):
    self.logger.info("The data collector is collecting info about" + letter)
    
    self.label = letter;
