from os import curdir, sep, path
import time, json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import config, files

class StaticServeHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # yeah, I know it's shitty. it's also 4 in the morning, deal with it.
        if "/neighbors" == self.path[:len("/neighbors")]:
            self.wfile.write(json.dumps(config.neighbors))
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
            handle = path.expanduser(config.shared_directory) + self.path
            with open(handle, 'rb') as f:
                self.send_response(200)
                self.end_headers()
                files.stream_file(f, self.wfile)
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


class SandwichServer(object):

    def __init__(self, ):
        pass

    def run(self, port):
        try:
            self.port = port
            self.server = HTTPServer(('', self.port), StaticServeHandler)
            print 'started httpserver...'
            self.server.serve_forever()
        except KeyboardInterrupt:
            print '^C received, shutting down server'
            self.server.socket.close()



if __name__ == '__main__':
    ss = SandwichServer()
    ss.run(8000)
