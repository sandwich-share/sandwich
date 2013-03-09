import sqlite3 as lite
import os

con = None


def find_files(directory):
  index = []
  for path, dirs, files in os.walk(directory):
    for f in files:
      fixed_path = path[path.find(directory)+len(directory)::]
      index.append([fixed_path, f])
  print "index: ", index


def create_db():
  try:
    with open('filename') as f: pass
  except IOError as e:

  try:
    lite.connect('ps.db')
    cursor = con.cursor()
  except:
    print "An Sqlite3 exception has occured."
  finally:
    if con:
      con.close()


