from os import curdir, sep, path
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import config

class StaticServeHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if not config.shared_directory:
            self.send_error(404, 'User not sharing files')
            return

        try:
            f = open(path.expanduser(config.shared_directory) + self.path, 'rb')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
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

