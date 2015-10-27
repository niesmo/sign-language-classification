import sys, os, inspect, thread, time
import models.frame

# get the src and lib directories
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, '../../lib'))

# including the lib folder to be able to import the lib dir
sys.path.insert(0, lib_dir)
import Leap

'''
What I was thinking this file would do:
1. the ability to `start` reading data from the leap
2. the ability to `stop` reading datr form the leap
3. Stoing those information into an array of some Model
4. Sending/returning those information to another client when needed
'''


'''
This is just a random listener to show what you need to do to get the data from the leap motion
Read: https://developer.leapmotion.com/documentation/python/api/Leap.Listener.html
'''
class SampleListener(Leap.Listener):
  def on_init(self, controller):
    print "Initialized"

  def on_connect(self, controller):
    print "Connected"
    # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

  def on_disconnect(self, controller):
    print "Disconnected"

  def on_exit(self, controller):
    print "Exited"

  def on_frame(self, controller):
    frame = controller.frame()
    myFrame = models.frame.FrameModel(frame)


    if(len(myFrame.hands) > 0):
      print str(myFrame.hands[0]['fingers'][0])
    # print myFrame.hands

    # for hand in frame.hands:
    #   print "Left Hand" if hand.is_left else "Right Hand"
    #   print "Palm position:", str(hand.palm_position)
    #   print "Palm Normal:", str(hand.palm_normal)
    #   print "Dirction:", str(hand.direction)

    #   print len(hand.fingers)
    #   for i,finger in enumerate(hand.fingers):

    #     print str(finger.type), str(finger.tip_position)

def main():
  # Create a sample listener and controller
  listener = SampleListener()

  # https://developer.leapmotion.com/documentation/python/api/Leap.Controller.html#Leap.Controller
  controller = Leap.Controller()

  # Have the sample listener receive events from the controller
  controller.add_listener(listener)

  # Keep this process running until Enter is pressed
  print "Press Enter to quit..."
  try:
    sys.stdin.readline()
  except KeyboardInterrupt:
    pass
  finally:
      # Remove the sample listener when done
      controller.remove_listener(listener)


if __name__ == "__main__":
  main()