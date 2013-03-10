import config, os, sys

def stream_file(fin, fout, size):
    try:
        print "Downloading..."
        num_blocks = 0
        while True:
            chunk = fin.read(config.chunk_size)
            if not chunk: break
            fout.write(chunk)
            num_blocks += 1
            if (num_blocks * config.chunk_size / (2**20)) % 10 == 0:
                print "Downloaded: %d MiB of %d MiB" % (num_blocks * config.chunk_size / (2**20)) % size
        print "Download Finished!"    
    except IOError as e:
        print sys.exc_info()
        return None
