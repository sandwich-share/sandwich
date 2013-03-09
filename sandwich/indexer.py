import os
import config

index = []
shared_directory = config.shared_directory

# crawl a directory and find all files and folders
def find_files():
  for path, dirs, files in os.walk(shared_directory):
    for f in files:
      if not f.startswith('.') and not os.path.split(path)[1].startswith('.'):
        add_file(path, f)
  return index

# add a file and folder to the index
def add_file(path, filename):
  index.append((os.path.relpath(path, shared_directory), filename))

# remove a file from the index
def remove_file(path, filename):
  index.remove((path, filename))
