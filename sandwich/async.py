import threading, multiprocessing


class AsyncHandler(object):

    def __init__(self):
        self.events = multiprocessing.Queue()
        self.thread = threading.Thread(target=self.event_handler, args=(self))

    def asynchronous_callback(self, f, args):
        self.events.put((f, args))


    def event_handler(self,):
        while True:
            e = events.get()
            # calls the function with unpacked arguments
            # as passed into the queue
            e[0](*e[1])


# globally available async queue (per import)
event = AsyncHandler()
