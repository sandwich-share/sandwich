from multiprocessing import Process, Queue

import indexer, file_monitor, webapp, config, client, signal, async, sys

def run_all():


    if (len(config.neighbors) > 0):
        client.SandwichGetter.bootstrap_into_network(config.neighbors[0])

    p1 = Process(target=indexer.find_files)

    webapp.run()

    p1.start()

    p1.join()

def signal_handler(signal, frame):
  print "\nStopping Server..."
  async.event.stop_thread()
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    run_all()
