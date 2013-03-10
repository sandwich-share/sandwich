import threading, Queue, sys


class AsyncHandler(object):

    def __init__(self):
        self.semaphore = threading.Semaphore(0)
        self.events = Queue.Queue()
        self.thread = threading.Thread(target=self.event_handler)
        self.thread.setDaemon(True)
        self.thread.start()


    def asynchronous_callback(self, f, args):
        self.events.put((f, args))
        self.semaphore.release()


    def event_handler(self,):
        while True:
            print "waiting for an event"
            self.semaphore.acquire()
            print "recieved event"
            e = self.events.get()
            # calls the function with unpacked arguments
            # as passed into the queue
            e[0](e[1])

    def stop_thread(self):
        sys.exit(0) 

# globally available async queue (per import)
event = AsyncHandler()
