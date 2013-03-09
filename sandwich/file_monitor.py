import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import indexer

class SimpleEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        super(SimpleEventHandler, self).on_created(event)

        if (not event.is_directory):
            p = event.src_path
            indexer.add_file(p, os.path.split(p)[1])

    def on_deleted(self, event):
        super(SimpleEventHandler, self).on_created(event)

        if (not event.is_directory):
            p = event.src_path
            indexer.remove_file(p, os.path.split(p)[1])

    def on_moved(self, event):
        super(SimpleEventHandler, self).on_created(event)

        if (not event.is_directory):
            ps = event.src_path
            pd = event.dest_path
            indexer.remove_file(ps, os.path.split(ps)[1])
            indexer.add_file(pd, os.path.split(pd)[1])

def start():
    observer = Observer()
    if (len(sys.argv) == 1):
        observer.schedule(SimpleEventHandler(), config.shared_directory, recursive=True)
    else:
        for i in range(1, len(sys.argv)):
            observer.schedule(SimpleEventHander(), sys.argv[i], recursive=True)
    observer.start()
