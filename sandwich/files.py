import config

def stream_file(fin, fout):
    while True:
        chunk = fin.read(config.chunk_size)
        if not chunk: break
        fout.write(chunk)
