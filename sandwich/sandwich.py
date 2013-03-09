from multiprocessing import Process, Queue

import server, indexer, file_monitor, webapp, config

def run():

    if (len(config.neighbors) > 0):
        client.SandwichGetter.bootstrap_into_network(config.neighbors[1])

    q = Queue()

    ss = server.SandwichServer()
    p = Process(target=server.SandwichServer.run, args=(ss, 8000, q))
    p.start()

    p.join()

if __name__ == '__main__':
    run()
