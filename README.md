# sign-language-classification
Using the Leap Motion, and various algorithms, classifying a limited set of American Sign Language gestures.

# instructions
## Creating Tables in the Database
go to `src/data/db` directory and run the `initialize.py` script
this script will create the tables in the database.
Note that if those tables already exist in the database, you will get an error
TODO: fix getting the error if the tables already exist

## Data Gathering
go to the src directry and run the `data-gathering.py` script.
You will be prompted to input the information about the person who is doing the experiment (not there now)
By pressing the `enter` key, the data gathering process starts and will stop in 5 seconds.
After that, it may take few minutes to input all that data in a database


##Gathering Data
  1. Nima (each letter twice) (Nov 7 around 3-4 pm)
  1. Saurabh (each letter twice) (Nov 7 around 3-4 pm)

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
