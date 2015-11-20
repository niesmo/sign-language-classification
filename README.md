# sign-language-classification
Using the Leap Motion, and various algorithms, classifying a limited set of American Sign Language gestures.

## Meeting with Eric (12 Nov, 2015)
* He mentioned to use PCA and LDA for reducing the number of dimentions
* he mentioned not using all the data points that we get from the Leap and instead average all those points to one points


# instructions
## Installing the Progressbar
go to `lib/progressbar` directory and run python setup.py install

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


## NEXT STEPS
@ IN PROGRESS:
  * Storing the trained units and K-Means (the network) in the disk somewhere
  * Include more alphabets
  * Reading from DB in NN
  * Make the code so that you can decide how many letter to train on (flexible for more letters in the future)

@ TODO:
  * Comparison of the Test with the Result in NN (for output -- our visualization)
  * Aggregating the input from Leap into ONE record (result in more variation in the data)
  * SVM (ask Eric if its good)
  * Experimenting with different configurations on NN and K-means
  * User interface
  * Reading in from leap and live outputting the result (For NN)
  * Learning from mistakes (at the end it asks if the prediction was correct. if not train again based on that) (NN) (Admin Only)
  * Predicting letter sequences form words and setences (something like autocorrect/autofill in there too)


## REPORT
* Saurabh
  - Kmeans graphs, tables, configuration, Kmeans write up

* Nima
  - Data Gathering , Dimensionality Reduction (if possible) write up

* Sanchit
  - Neural nets config, graphs, NN write up

* Common
  - conclusion, references.