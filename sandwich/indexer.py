import sys
import os
import config
import sqlite3
import json

shared_directory = os.path.expanduser(config.shared_directory)
db = "index.db"
table = "local"
index = []

# crawl a directory and find all files and folders
def find_files():
    global index
    index = []
    for path, dirs, files in os.walk(shared_directory):
        for f in files:
            if not f.startswith('.') and not os.path.split(path)[1].startswith('.'):
              index.append((os.path.relpath(path, shared_directory), f))
    try:
        os.remove(db)
    except:
        print "Database does not exist, creating it."
    finally:
        f = open(db, "w+")
        f.close()
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE ''' + table + ''' (path text, filename text)''')
        cursor.executemany("INSERT INTO " + table + "  VALUES (?,?)", index)
        con.commit()
    except:
        for m in sys.exc_info():
            print m
    finally:
        con.close()

# add a file and folder to the index
def add_file(path, filename):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cmd = "INSERT INTO " + table + " VALUES (?,?)"
        cursor.execute(cmd, (path, filename))
        con.commit()
    except:
        for m in sys.exc_info():
            print m
    finally:
        con.close()

# remove a file from the index
def remove_file(path, filename):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cmd = "DELETE FROM " + table + " WHERE path=? AND filename=?"
        cursor.execute(cmd, (path, filename))
        con.commit()
    except:
        for m in sys.exc_info():
             print m
    finally:
        con.close()

# finds a file with the given name in the database
def search(search_param):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cmd = "SELECT * FROM " + table + " WHERE path LIKE ? OR filename LIKE ?"
        results = []
        search = '%' + str.replace(search_param, ' ', '%') + '%'
        for res in cursor.execute(cmd, (search, search)):
            results.append(res)
        return json.dumps(results)
    except:
        for m in sys.exc_info():
            print m
    finally:
        con.close()
