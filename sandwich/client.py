import httplib, json
import config, files
import socket


class SandwichGetter(object):

    @classmethod
    def get_res(cls, ip, res):
        print "\n\nInside get_res function\n\n"
        conn = None
        try:
            conn = httplib.HTTPConnection(ip, timeout=config.timeout)
            conn.request("GET", res)
            r1 = conn.getresponse()

            fullpath = path.expanduser(config.shared_directory) + res
            if path.exists(fullpath):
                print "Not overwriting existing file"
            else:
                with open(fullpath, 'wb') as f:
                     files.stream_file(r1, f)
        except:
            print "Error while downloading file"

        if conn != None:
            conn.close()

    @classmethod
    def get_many_res(cls, ip, reses):
        for res in reses:
            self.get_res(cls, ip, res)


    @classmethod
    def bootstrap_into_network(cls, ip):
        conn = None
        try:
            conn = httplib.HTTPConnection("%s:%d" % (ip, config.serverport), timeout=config.timeout)
            conn.request("GET", "/neighbors")
            r1 = conn.getresponse()
            config.neighbors.extend(json.loads(r1.read()))
            config.neighbors.append(ip)
            config.neighbors = list(set(config.neighbors))
        except:
            print "Error bootstrapping to %s:%d" % (ip, config.serverport)

        if conn != None:
            conn.close()

