from flask import Flask, Markup, render_template, request
import os
import json
import httplib
import urllib
import re

import indexer, config

app = Flask('webapp', template_folder=os.getcwd() + "/templates")

@app.route("/")
def index():
    return render_template("index.html", peers=config.neighbors, port=config.webapp)

@app.route("/query", methods=["GET"])
def query():
    return indexer.search(re.match("search=(.*)", request.data).group(1))

@app.route("/search", methods=["GET"])
def search():
    x = ""
    print 1
    if not request.args.get("host"):
        print 2
        conn = httplib.HTTPConnection("localhost:%d" % config.serverport, timeout=config.timeout)
        conn.request("GET", "/neighbors")
        neighbors = json.loads(conn.getresponse().read())
        conn.close()
        for n in neighbors:
            conn = httplib.HTTPConnection("%s:%d" % (n, config.webapp), timeout=config.timeout)
            conn.request("GET", "/query", urllib.urlencode({'search': request.args.get("search")}))
            x += conn.getresponse().read()
            conn.close()
    else:
        print 3
        conn = httplib.HTTPConnection("%s:%d" % (request.args.get("host"), config.webapp), timeout=config.timeout)
        conn.request("GET", "/query", urllib.urlencode({'search': ""}))
        x = conn.getresponse().read()
        conn.close()
    return x

@app.route("/neighbors")
def neighbors():
    conn = httplib.HTTPConnection("localhost:%d" % config.serverport)
    conn.request("GET", "/neighbors")
    ret = conn.getresponse().read()
    conn.close()
    return ret

def run():
    app.debug = config.debug
    # flask is dumb and tries to restart infinitely if we fork it into a subprocess.
    # this is bad. So we disable it, and hate on flask a bit.
    app.run(port=config.webapp, use_reloader=False, host='0.0.0.0')

if __name__ == '__main__':
    app.debug = True
    app.run()
