# sign-language-classification
Using the Leap Motion, and various algorithms, classifying a limited set of American Sign Language gestures.

Letters to classify:
  Step 1: A, B, L, X, V, W, Y
  Step 2: I, O

For data collection:
  check if the hand is within the box
  store the confidence  ( > 75% )


Data that we need to store:
  1. Palm position / stabalize palm position
  2. Palm direction / Palm normal direction
  5. Wrist Position (optional)
  6. Frame.fingers (for each type (which finger is it))
    a. stablizedTipPosition
    b. Joint position
      I. carpPosition
      II. dipPostion
      III. mcpPostion
      IV. pipPosition
    c. Extended (boolean)
    d. direction
  7. Frame.hand.SphereRadius



All:
  - Data Collection

Sanchit:
  - Toolkits for the algos
  - Data collection
Saurabh:
  - 
Nima: