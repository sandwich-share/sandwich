import os
import config
import sqlite3

index = []
shared_directory = os.path.expanduser(config.shared_directory)
db = "index.db"
table = "local"

# crawl a directory and find all files and folders
def find_files():
    global index
    index = []
    for path, dirs, files in os.walk(shared_directory):
        for f in files:
            if not f.startswith('.') and not os.path.split(path)[1].startswith('.'):
              index.append((os.path.relpath(path, shared_directory), f))
    config.index = index
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
        print "Sqlite3 Error!"
    finally:
        con.close()

# add a file and folder to the index
def add_file(path, filename):
    index.append((os.path.relpath(path, shared_directory), filename))
    config.index = index
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute("INSERT INTO " + table + " VALUES ('" + os.path.relpath(path, shared_directory) + "','" + filename + "')")
        con.commit()
    except:
        print "Sqlite3 Error: Cannot insert values!"
    finally:
        con.close()

# remove a file from the index
def remove_file(path, filename):
    index.remove((path, filename))
    config.index = index
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute("DELETE FROM " + table + "  WHERE 'path=" + path + "' AND 'filename=" + filename + "'")
        con.commit()
    except:
        print "SQlite3 Error: Cannot delete values!"
    finally:
        con.close()

# finds a file with the given name in the database
def search_file(filename):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM " + table + " WHERE filename='" + filename + "'")
    except:
        print "SQlite3 Error: Cannot select from table!"
    finally:
        con.close()
