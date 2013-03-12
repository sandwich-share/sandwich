import urllib
import socket
import sys
import os
import config
import sqlite3
import json

db = "index.db"
table = "local"

# crawl a directory and find all files and folders
def find_files():
    index = []
    for path, dirs, files in os.walk(config.shared_directory):
        for f in files:
            if not f.startswith('.') and (not os.path.split(path)[1].startswith('.') or path == "."+os.sep or path == '.'):
                size = os.path.getsize(os.path.join(path,f))
                if size >= 1000000000:
                    size = float(size) / 1000000000
                    m = "G"
                elif size >= 1000000:
                    size = float(size) / 1000000
                    m = "M"
                elif size >= 1000:
                    size = float(size) / 1000
                    m = "K"
                else:
                    m = ""

                index.append((os.path.relpath(path, config.shared_directory), f, "%d%s" % (round(size,4),m)))
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
        cursor.execute('''CREATE TABLE ''' + table + ''' (path text, filename text, size text)''')
        cursor.executemany("INSERT INTO " + table + "  VALUES (?,?,?)", index)
        con.commit()
    except:
        for m in sys.exc_info():
            print m
    finally:
        con.close()

# add a file and folder to the index
def add_file(path, filename, size):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cmd = "INSERT INTO " + table + " VALUES (?,?,?)"
        cursor.execute(cmd, (path, filename, size))
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
def search(search_param, ip_address):
    try:
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cmd = "SELECT * FROM " + table + " WHERE path LIKE ? OR filename LIKE ?"
        results = []
        search = '%' + str.replace(search_param, '+', '%') + '%'
        for res in cursor.execute(cmd, (search, search)):
            results.append(res + ('http://' + ip_address + ":" + str(config.webapp) + '/files/' + str.replace(str(urllib.quote(res[0])) + '/', './', '') + urllib.quote(res[1]),))
        return json.dumps(results)
    #http://myip:serverport/files/path/filename
    except:
        for m in sys.exc_info():
            print m
    finally:
        con.close()
