import httplib, json
import config, files


class SandwichGetter(object):

    @classmethod
    def get_res(cls, ip, res):
    
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

            conn.close()
        except socket.error:
            print "Socket error while downloading"

    @classmethod
    def get_many_res(cls, ip, reses):
        for res in reses:
            self.get_res(cls, ip, res)


    @classmethod
    def bootstrap_into_network(cls, ip):
        try:
            conn = httplib.HTTPConnection("%s:%d" % (ip, config.serverport), timeout=config.timeout)
            conn.request("GET", "/neighbors")
            r1 = conn.getresponse()
            config.neighbors.extend(json.loads(r1.read()))
            config.neighbors.append(ip)
            config.neighbors = list(set(config.neighbors))
            conn.close()
        except socket.error:
            print "Error bootstrapping to %s:%d" % (ip, config.serverport)
