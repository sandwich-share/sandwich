from flask import Flask, Markup, render_template, request
import os
import json
import httplib
import urllib

import indexer, config

app = Flask('webapp', template_folder=os.getcwd() + "/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    return indexer.search(str(request.form.get("search")))

@app.route("/search", methods=["POST"])
def search():
    conn = httplib.HTTPConnection("localhost:%d" % config.serverport)
    conn.request("GET", "/neighbors")
    neighbors = json.loads(conn.getresponse().read())
    x = ""
    for n in neighbors:
        conn = httplib.HTTPConnection("%s:%d" % (n, config.webapp))
        conn.request("POST", "/query", urllib.urlencode({'search': request.form.get("search")}))
        x += conn.getresponse().read()
    return x

@app.route("/neighbors")
def neighbors():
    conn = httplib.HTTPConnection("localhost:%d" % config.serverport)
    conn.request("GET", "/neighbors")
    return conn.getresponse().read()

def run():
    app.debug = config.debug
    # flask is dumb and tries to restart infinitely if we fork it into a subprocess.
    # this is bad. So we disable it, and hate on flask a bit.
    app.run(port=config.webapp, use_reloader=False)

if __name__ == '__main__':
    app.debug = True
    app.run()
