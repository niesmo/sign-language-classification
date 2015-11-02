import sys, os, inspect, thread, time, logging

# get the src and other directories
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(curr_dir, '../../../lib'))
db_dir = os.path.abspath(os.path.join(curr_dir, '../db'))

# including the lib and the models folder to be able to import the lib and models dir
sys.path.insert(0, lib_dir)

import Leap
import data.models.frame
import data.dataCollectionTools

class DataCollectorListener(Leap.Listener):
  """
  Order: 1
  This function is called when the Listener is being initialized
  """
  def on_init(self, controller):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.debug("On Init")


  """
  Order: 2
  This function is called when the listener is Connected after being initialized 
  """
  def on_connect(self, controller):
    self.logger.debug("On Connect")

  """
  Order: ?
  I dont know when this function is called 
  """
  def on_disconnect(self, controller):
    self.logger.debug("On Disconnect")

  """
  Order: 4 (Last)
  This function is called when the listener is exiting (i guess)
  """
  def on_exit(self, controller):
    self.logger.debug("On Exit")


  """
  Order: 3
  This function is called everytime a new frame is available
  Which means, this function cant take long, because otherwise the next frame will be missed
  """
  def on_frame(self, controller):
    self.logger.debug("On Frame")

    # get the frame
    frame = controller.frame()

    # create a formatted frame using the FrameModel
    myFrame = data.models.frame.FrameModel(frame)

    # get the data collector and add the Frame to that
    dataCollector = data.dataCollectionTools.DataCollector.Instance()
    dataCollector.addFrame(myFrame)
