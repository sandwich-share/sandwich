import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import indexer
import config

def hrsize(size):
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
    return "%d%s" % (size,m)

class SimpleEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        super(SimpleEventHandler, self).on_created(event)

        if (not event.is_directory):
            p = event.src_path
            indexer.add_file(os.path.relpath(os.path.split(p)[0], config.shared_directory), os.path.split(p)[1], hrsize(os.path.getsize(p)))

    def on_deleted(self, event):
        super(SimpleEventHandler, self).on_created(event)

        if (not event.is_directory):
            p = event.src_path
            indexer.remove_file(os.path.relpath(os.path.split(p)[0], config.shared_directory), os.path.split(p)[1])

    def on_moved(self, event):
        super(SimpleEventHandler, self).on_created(event)

        if (not event.is_directory):
            ps = event.src_path
            pd = event.dest_path
            indexer.remove_file(os.path.relpath(os.path.split(ps)[0], config.shared_directory), os.path.split(ps)[1])
            indexer.add_file(os.path.relpath(os.path.split(pd)[0], config.shared_directory), os.path.split(pd)[1], hrsize(os.path.getsize(p)))

def start():
    observer = Observer()
    if (len(sys.argv) == 1):
        observer.schedule(SimpleEventHandler(), config.shared_directory, recursive=True)
    else:
        for i in range(1, len(sys.argv)):
            observer.schedule(SimpleEventHander(), sys.argv[i], recursive=True)
    observer.start()
