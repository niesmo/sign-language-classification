import sqlite3 as lite
import argparse

def initialize_database_tables(dbFileName):
  fingers = ["thumb", "index", "middle", "ring", "pinky"]
  connection = lite.connect(dbFileName)

  handDataQuery = "CREATE TABLE HandData "
  handDataQuery += "( id INTEGER PRIMARY KEY AUTOINCREMENT, "
  handDataQuery += "confidence REAL NOT NULL, "
  handDataQuery += "palm_position INTEGER NOT NULL, "
  handDataQuery += "palm_direction INTEGER NOT NULL, "
  handDataQuery += "palm_normal_direction INTEGER NOT NULL, "
  handDataQuery += "wrist_position INTEGER NOT NULL, "
  handDataQuery += "hand_sphere_radius REAL NOT NULL, "

  for finger in fingers:
    handDataQuery += finger + "_tip_position INTEGER NOT NULL, "
    handDataQuery += finger + "_metacarpal_position INTEGER NOT NULL, "
    handDataQuery += finger + "_proximal_position INTEGER NOT NULL, "
    handDataQuery += finger + "_intermediate_position INTEGER NOT NULL, "
    handDataQuery += finger + "_distal_position INTEGER NOT NULL, "
    handDataQuery += finger + "_is_extended INTEGER, " # sqlite does not have bools
    handDataQuery += finger + "_direction INTEGER NOT NULL, "

  # adding the label
  handDataQuery += "lable TEXT NOT NULL, "
  
  # adding the timestamp
  handDataQuery += "timestamp TEXT NOT NULL, "

  # adding the attempt id
  handDataQuery += "attemptID TEXT NOT NULL )"

  print handDataQuery

  coordinateQuery = "CREATE TABLE Coordinate "
  coordinateQuery += "( id INTEGER PRIMARY KEY AUTOINCREMENT, "
  coordinateQuery += "x REAL, "
  coordinateQuery += "y REAL, "
  coordinateQuery += "z REAL )"

  print coordinateQuery
  
  with connection:
    cursor = connection.cursor()
    cursor.execute(handDataQuery);
    cursor.execute(coordinateQuery);

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Initialization of the database tables')
  parser.add_argument('-d', default='data.db' ,action='store', dest='dbFileName')

  args = parser.parse_args()
  dbFileName = args.dbFileName

  initialize_database_tables(dbFileName)