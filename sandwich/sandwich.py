from multiprocessing import Process, Queue

import server, indexer, file_monitor, webapp, config, client

def run_all():


    if (len(config.neighbors) > 0):
        client.SandwichGetter.bootstrap_into_network(config.neighbors[0])

    q = Queue()


    p2 = Process(target=server.run, args=(config.serverport, q,))


    p3 = Process(target=webapp.run)

    p1 = Process(target=indexer.find_files)


    p1.start()

    p2.start()

    p3.start()

    p1.join()
    p2.join()
    p3.join()


if __name__ == "__main__":
    run_all()
