import threading, Queue, sys


class AsyncHandler(object):
    """Provide a way to execute asynchronous events.

    YOU PROBABLY DON'T WANT TO INSTANTIATE THIS CLASS.
    Instead, use the already instantiated instance 'async.event'.

    Note that async.event exists on an import by import basis and is not shared
    between files. It also doesn't necessarily aquire the correct locks, so if
    you want to make sure you are threadsafe, aquire locks inside the function
    you register for callback.
    """

    def __init__(self):
        self.semaphore = threading.Semaphore(0)
        self.events = Queue.Queue()
        self.thread = threading.Thread(target=self.event_handler)
        self.thread.setDaemon(True)
        self.thread.start()


    def asynchronous_callback(self, f, args):
        """Register function 'f' with 'args' (as tuple) for asynchonous callback
        """
        self.events.put((f, args))
        self.semaphore.release()


    def event_handler(self,):
        """The main loop for our AsyncHandler. Runs in a separate thread and
        handles async requests as they come in.
        """
        while True:
            print "AsyncHandler waiting for an event"
            self.semaphore.acquire()
            print "AsyncHandler recieved event, executing..."
            e = self.events.get()
            # calls the function with unpacked arguments
            # as passed into the queue
            e[0](e[1])

    def stop_thread(self):
        sys.exit(0)

# globally available async queue (per import)
event = AsyncHandler()
