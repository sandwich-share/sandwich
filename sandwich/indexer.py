import os
index = []

# crawl a directory and find all files and folders
def find_files(directory):
  for path, dirs, files in os.walk(directory):
    for f in files:
      add_file(path, directory, f)
  return index

# add a file and folder to the index
def add_file(path, shared_directory, filename):
  index.append((os.path.relpath(path, shared_directory), filename))

# remove a file from the index
def remove_file(path, filename):
  index.remove((path, filename))
