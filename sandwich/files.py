import config, os

def stream_file(fin, fout):
    try:
        while True:
            chunk = fin.read(config.chunk_size)
            if not chunk: break
            fout.write(chunk)

    except IOError as e:
        return None
