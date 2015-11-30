import sqlite3 as lite
import sys, os, inspect, thread, time, logging
import ConfigParser
import datetime


# get the src and other directories
curr_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(curr_dir, '../../../lib'))
db_dir = os.path.abspath(os.path.join(curr_dir, '../db'))
config_file = os.path.abspath(os.path.join(curr_dir, '../../config/config.conf'))


# including the lib and the models folder to be able to import the lib and models dir
sys.path.insert(0, lib_dir)
import Leap

# setting up the configuration object
Config = ConfigParser.ConfigParser()
Config.read(config_file)

# https://github.com/void-main/PyLeapDataDumper/blob/master/data_dumper.py
RAD_TO_DEG = 57.2957801819

class FrameModel:
  def __init__(self, frame):
    self.logger = logging.getLogger(self.__class__.__name__)

    # Save the frame as a property of this class
    self.frame = frame

    # database name
    self.dbName = None

    # serialized the data into private properties of this model
    self.serialize()

  def setDbName(self, name):
    self.dbName = name;

  '''
  This function will simply save this object in to the database
  '''
  def save(self, label, uuid):
    # dont bother is there is no hand in the frame
    if len(self.hands) == 0:
      return

    # warning if there are more than one hands
    if len(self.hands) > 1:
      self.logger.warning("There are more than one hand in the frame. There are", len(self.hands), "hands")

    # getting the timestamp
    now = datetime.datetime.now()

    '''
    0 -> confidence
    1 -> palm position
    2 -> palm direction
    3 -> palm normal direction
    4 -> wrist position
    5 -> hand_sphere_radius
    6 - 12 -> Thumb 
    13 - 19 -> Index 
    20 - 26 -> Middle
    27 - 33 -> Ring
    34 - 40 -> Pinky 
    '''
    

    valuesPlaceholdersArray = ['{'+str(i)+'}' for i in range(41)]
    valuesPlaceholders = ", ".join(valuesPlaceholdersArray)

    query = "INSERT INTO HandData VALUES(null, "+valuesPlaceholders+", '" + label +"', '"+ str(now) +"', '" + uuid + "')"

    # In the Data Collector, decide whether to even call save when
    # there is more than one hand
    if len(self.hands) == 1:
      handIdx = 0

    elif (self.hands[0]['confidence'] > self.hands[1]['confidence']):
      handIdx = 0

    else:
      handIdx = 1

    selectedHand = self.hands[handIdx]

    # store all the finger information
    thumbFingerRowIds = self._saveFinger(handIdx, Leap.Finger.TYPE_THUMB)
    indexFingerRowIds = self._saveFinger(handIdx, Leap.Finger.TYPE_INDEX)
    middleFingerRowIds = self._saveFinger(handIdx, Leap.Finger.TYPE_MIDDLE)
    ringFingerRowIds = self._saveFinger(handIdx, Leap.Finger.TYPE_RING)
    pinkyFingerRowIds = self._saveFinger(handIdx, Leap.Finger.TYPE_PINKY)
    

    query = query.format(
      selectedHand['confidence'],
      self._saveCoordinate(selectedHand[Config.get('frame_fields', 'palm_position')]),
      self._saveCoordinate(selectedHand['direction']),
      self._saveCoordinate(selectedHand['normal_direction']),
      self._saveCoordinate(selectedHand['wrist_position']),
      selectedHand['sphere_radius'],
      
      thumbFingerRowIds[0], # tip position
      thumbFingerRowIds[1], # metacarpal position
      thumbFingerRowIds[2], # proximal position
      thumbFingerRowIds[3], # intermediate position
      thumbFingerRowIds[4], # distal position
      thumbFingerRowIds[5], # is extended => NULL
      thumbFingerRowIds[6], # direction

      indexFingerRowIds[0], # tip position
      indexFingerRowIds[1], # metacarpal position
      indexFingerRowIds[2], # proximal position
      indexFingerRowIds[3], # intermediate position
      indexFingerRowIds[4], # distal position
      indexFingerRowIds[5], # is extended => NULL
      indexFingerRowIds[6], # direction

      middleFingerRowIds[0], # tip position
      middleFingerRowIds[1], # metacarpal position
      middleFingerRowIds[2], # proximal position
      middleFingerRowIds[3], # intermediate position
      middleFingerRowIds[4], # distal position
      middleFingerRowIds[5], # is extended => NULL
      middleFingerRowIds[6], # direction

      ringFingerRowIds[0], # tip position
      ringFingerRowIds[1], # metacarpal position
      ringFingerRowIds[2], # proximal position
      ringFingerRowIds[3], # intermediate position
      ringFingerRowIds[4], # distal position
      ringFingerRowIds[5], # is extended => NULL
      ringFingerRowIds[6], # direction

      pinkyFingerRowIds[0], # tip position
      pinkyFingerRowIds[1], # metacarpal position
      pinkyFingerRowIds[2], # proximal position
      pinkyFingerRowIds[3], # intermediate position
      pinkyFingerRowIds[4], # distal position
      pinkyFingerRowIds[5], # is extended => NULL
      pinkyFingerRowIds[6], # direction
    );

    connection = lite.connect(os.path.join(db_dir, self.dbName))
    with connection:
      cursor = connection.cursor()
      cursor.execute(query)

    return

  '''
  This function will save the coordinate to the Coordinate table
  and will return the id of the row inserted
  '''
  def _saveCoordinate(self, coordinate):
    query = "INSERT INTO Coordinate VALUES(null, {0}, {1}, {2})"
    query = query.format(str(coordinate[0]), str(coordinate[1]), str(coordinate[2]))

    connection = lite.connect(os.path.join(db_dir, self.dbName))
    with connection:
      cursor = connection.cursor()
      cursor.execute(query)

      return cursor.lastrowid

  '''
  This function save the coordinates about a finger and returns
  the ids of those rows in the same order as they should be inseted
  in the HandData table
  Returns an array of ids of these coordinates (in order)
    0: tip position
    1: metacarpal position
    2: proximal position
    3: intermediate position
    4: distal position
    5: is extended
    6: direction
  '''
  def _saveFinger(self, handIdx, fingerType):
    returnIds = []

    returnIds.append(self._saveCoordinate(self.hands[handIdx]['fingers'][fingerType][Config.get('frame_fields', 'finger_tip_position')]))
    returnIds.append(self._saveCoordinate(self.hands[handIdx]['fingers'][fingerType]['metacarpal']))
    returnIds.append(self._saveCoordinate(self.hands[handIdx]['fingers'][fingerType]['proximal']))
    returnIds.append(self._saveCoordinate(self.hands[handIdx]['fingers'][fingerType]['intermediate']))
    returnIds.append(self._saveCoordinate(self.hands[handIdx]['fingers'][fingerType]['distal']))
    returnIds.append('null') # cant get the is_extended in python
    returnIds.append(self._saveCoordinate(self.hands[handIdx]['fingers'][fingerType]['direction']))
    
    return returnIds

  '''
  This function checks to see if this is a good frame or not
  For example, about the confidence or the hand being in the interaction box
  '''
  def checkFrame(self):
    pass


  '''
  This function simply serialized the data that we get
  from the Leap into the FrameModel
  '''
  def serialize(self):
    # temporary variable for the frame
    frame = self.frame

    # id of the frame
    self.id = frame.id

    # timestamp
    self.timestamp = frame.timestamp

    # dictionary for the hand
    self.hands = [];

    if not len(frame.hands) == 0:
      for hand in frame.hands:
        # the main dictionary for the hand information
        hand_dict = {}

        # type of the hand
        hand_dict['type'] = "left" if hand.is_left else "right"

        # validity of the hand
        hand_dict['is_valid'] = hand.is_valid
        
        # confidence of the frame on this hand
        hand_dict['confidence'] = hand.confidence

        # info about the sphere
        hand_dict['sphere_radius'] = hand.sphere_radius
        hand_dict['sphere_center'] = hand.sphere_center

        # infor about the palm position
        hand_dict['palm_position'] = hand.palm_position
        hand_dict['palm_stabilized_position'] = hand.stabilized_palm_position

        # wrist position
        hand_dict['wrist_position'] = hand.wrist_position

        # Information about the hand's normal vector and direction
        normal = hand.palm_normal
        direction = hand.direction

        hand_dict['normal_direction'] = normal
        hand_dict['direction'] = direction

        # Calculate the hand's pitch, roll, and yaw angles
        hand_dict['angle'] = {}
        hand_dict['angle']['pitch'] = direction.pitch * RAD_TO_DEG
        hand_dict['angle']['roll'] = normal.roll * RAD_TO_DEG
        hand_dict['angle']['yaw'] = direction.yaw * RAD_TO_DEG
        

        fingers = hand.fingers
        hand_dict['fingers'] = {}
        if not len(fingers) == 0:

          # fingerTypeMap = {
          #   Leap.Finger.TYPE_THUMB: "thumb",
          #   Leap.Finger.TYPE_INDEX: "index",
          #   Leap.Finger.TYPE_MIDDLE: "middle",
          #   Leap.Finger.TYPE_RING: "ring",
          #   Leap.Finger.TYPE_PINKY: "pinky"
          # }

          for finger in fingers:
            # get the information about the joints of the finger
            hand_dict['fingers'][finger.type] = {
              "metacarpal": finger.bone(Leap.Bone.TYPE_METACARPAL).center,
              "proximal": finger.bone(Leap.Bone.TYPE_PROXIMAL).center, 
              "intermediate": finger.bone(Leap.Bone.TYPE_INTERMEDIATE).center,
              "distal": finger.bone(Leap.Bone.TYPE_DISTAL).center
            }

            hand_dict['fingers'][finger.type]['direction'] = finger.direction
            hand_dict['fingers'][finger.type]['tip_position'] = finger.tip_position
            hand_dict['fingers'][finger.type]['stabilized_tip_position'] = finger.stabilized_tip_position
            hand_dict['fingers'][finger.type]['is_valid'] = finger.is_valid


        self.hands.append(hand_dict)