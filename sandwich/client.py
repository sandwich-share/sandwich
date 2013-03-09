import httplib

import config, files


class SandwichGetter(object):

    @classmethod
    def get_res(ip, res):
        conn = httplib.HTTPConnection(ip)
        conn.request("GET", res)
        r1 = conn.getresponse()
        #TODO There should totally be error handling here
        # we also will probably overwrite a file if it exists.
        # oops.
        with open(path.expanduser(config.shared_directory) + res, 'wb') as f:
            files.stream_file(r1, f)

    @classmethod
    def get_many_res(ip, reses):
        for res in reses:
            self.get_res(ip, res)
