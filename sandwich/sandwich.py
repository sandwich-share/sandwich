from multiprocessing import Process, Queue

import indexer, file_monitor, webapp, config, client

def run_all():


    if (len(config.neighbors) > 0):
        client.SandwichGetter.bootstrap_into_network(config.neighbors[0])

    p1 = Process(target=indexer.find_files)

    webapp.run()

    p1.start()

    p1.join()


if __name__ == "__main__":
    run_all()
