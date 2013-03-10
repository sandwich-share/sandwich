import config, os

def stream_file(fin, fout):
    shared = config.shared_directory
    try:
        with open(shared + "/" + fin, "r") as f:
            size = os.stat(shared + fin).st_size


            if size == os.stat(fin).st_size:
                return

            fin.seek(size + 1)
            while True:
                chunk = fin.read(config.chunk_size)
                if not chunk: break
                fout.write(chunk)

    except IOError as e:
        return None

    while True:
        chunk = fin.read(config.chunk_size)
        if not chunk: break
        fout.write(chunk)
