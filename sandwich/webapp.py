from flask import Flask
from flask import Markup
from flask import render_template
import os

import indexer

indexer.find_files()
app = Flask('webapp', template_folder=os.getcwd() + "/templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    return render_template("query_result.html", index=indexer.index)


if __name__ == '__main__':
    app.debug = True
    app.run()
