from flask import Flask
from flask import Markup
from flask import render_template
import os

import indexer, config

app = Flask('webapp', template_folder=os.getcwd() + "/templates")

@app.route("/")
def index():
  indexer.find_files()
  print len(indexer.index)
  return render_template("index.html", index=indexer.index)


def run():
  app.debug = config.debug
  # flask is dumb and tries to restart infinitely if we fork it into a subprocess.
  # this is bad. So we disable it, and hate on flask a bit.
  app.run(port=config.webapp, use_reloader=False)

if __name__ == '__main__':
  app.debug = True
  app.run()
