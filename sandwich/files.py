
def stream_file(fin, fout):
    CHUNK_SIZE = 2**20
    while True:
        chunk = fin.read(CHUNK_SIZE)
        if not chunk: break
        fout.write(chunk)
