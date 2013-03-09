from flask import Flask
from flask import Markup
from flask import render_template
from flask import request
import os
import json

import indexer, config

app = Flask('webapp', template_folder=os.getcwd() + "/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    return render_template("query_result.html", index=json.loads(indexer.search(str(request.form.get("search")))))


def run():
    app.debug = config.debug
    # flask is dumb and tries to restart infinitely if we fork it into a subprocess.
    # this is bad. So we disable it, and hate on flask a bit.
    app.run(port=config.webapp, use_reloader=False, host='0.0.0.0')

if __name__ == '__main__':
    app.debug = True
    app.run()
