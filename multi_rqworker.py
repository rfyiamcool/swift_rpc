import os
import logging
import sys
import signal
import redis
import multiprocessing
from rq import Worker, Queue, Connection
listen = ['high', 'default', 'low']
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
conn = redis.from_url(redis_url)

def sigint_handler(signum,frame):    
    for i in pid_list:
        os.kill(i,signal.SIGKILL)
    logging.info("exit...")
    sys.exit()    

def worker():
    logging.info('this is worker')
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

pid_list = []
signal.signal(signal.SIGINT,sigint_handler) 
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    for i in xrange(3):
        pool.apply_async(worker,)
    for i in multiprocessing.active_children():
        pid_list.append(i.pid)
    pid_list.append(os.getpid())
    pool.close()
    pool.join()
