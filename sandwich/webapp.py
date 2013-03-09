from flask import Flask
from flask import Markup
from flask import render_template
import os

import indexer

app = Flask(__name__)
app = Flask('webapp', template_folder=os.getcwd() + "/templates")

@app.route("/")
def index():
  indexer.find_files()
  print len(indexer.index)
  return render_template("index.html", index=indexer.index)


if __name__ == '__main__':
  app.debug = True
  app.run()
