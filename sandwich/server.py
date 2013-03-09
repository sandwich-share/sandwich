from os import curdir, sep, path
import Queue
import time, json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import config, files, client

class StaticServeHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # yeah, I know it's shitty. it's also 4 in the morning, deal with it.
        if "/neighbors" == self.path[:len("/neighbors")]:
            print config.neighbors
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(config.neighbors))
            print self.client_address[0]
            if not self.client_address[0] in config.neighbors:
                client.SandwichGetter.bootstrap_into_network(self.client_address[0])
            return

        if "/files" == self.path[:len("/files")]:
            self.path = self.path[len("/files"):]
        else:
            self.send_error(404, 'Bad path. Sucks to suck.')
            return

        if not config.shared_directory:
            self.send_error(404, 'User not sharing files')
            return

        try:
            handle = config.shared_directory + self.path
            with open(handle, 'rb') as f:
                self.send_response(200)
                self.end_headers()
                files.stream_file(f, self.wfile)
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


def run(port, q=None):
    try:
        ss = HTTPServer(('', port), StaticServeHandler)
        print 'started httpserver on port ', port
        while True:
            # update our state from the parent process
            if q:
                try:
                    r = q.get(block=False)
                    if r[0] == "shared_directory":
                        config.shared_directory = r[1]
                    elif r[0] == "neighbors":
                        config.neighbors = r[1]
                except Queue.Empty:
                    pass

            ss.handle_request()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        ss.socket.close()



if __name__ == '__main__':
    run(8000)

