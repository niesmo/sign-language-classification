# https://github.com/void-main/PyLeapDataDumper/blob/master/data_dumper.py
RAD_TO_DEG = 57.2957801819

class FrameModel:
  def __init__(self, frame):
    # Save the frame as a property of this class
    self.frame = frame

    # serialized the data into private properties of this model
    self.serialize()


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

    # array for the hands
    self.hands = [];

    # array for the tools
    self.tools = [];

    if not len(frame.hands) == 0:
      for hand in frame.hands:
        hand_dict = {}

        fingers = hand.fingers
        hand_dict['fingers'] = []
        if not len(fingers) == 0:
          for finger in fingers:
              hand_dict['fingers'].append(finger.tip_position)

        hand_dict['sphere_radius'] = hand.sphere_radius
        hand_dict['sphere_center'] = hand.sphere_center

        hand_dict['palm_position'] = hand.palm_position
        hand_dict['paml_velocity'] = hand.palm_velocity

        # Get the hand's normal vector and direction
        normal = hand.palm_normal
        direction = hand.direction

        hand_dict['palm_normal'] = normal
        hand_dict['direction'] = direction

        # Calculate the hand's pitch, roll, and yaw angles
        hand_dict['hand_angle'] = {}
        hand_dict['hand_angle']['pitch'] = direction.pitch * RAD_TO_DEG
        hand_dict['hand_angle']['roll'] = normal.roll * RAD_TO_DEG
        hand_dict['hand_angle']['yaw'] = direction.yaw * RAD_TO_DEG

        # print hand_dict
        self.hands.append(hand_dict)



