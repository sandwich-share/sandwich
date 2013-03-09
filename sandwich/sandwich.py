from multiprocessing import Process, Queue

import server, indexer, file_monitor, webapp

def run():
    q = Queue()
    ss = server.SandwichServer()
    p = Process(target=server.SandwichServer.run, args=(ss, 8000, q))
    p.start()

    p.join()

if __name__ == '__main__':
    run()
