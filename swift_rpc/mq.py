#coding:utf-8
from serialize import serialize, deserialize
from config import *
from rq import Queue
from rq.job import Job
import redis

class MessageQueue(object):

    def __init__(self, host, port):
        self._conn = redis.Redis(connection_pool=redis.BlockingConnectionPool(max_connections=15, host=host, port=port))

    def set(self,k,v):
        self._conn.set(k,v)

    def get(self,k):
        return self._conn.get(k)
    
    def push(self, queue, msg):
        self._conn.rpush(queue, serialize(msg))

    def spop(self, queue):
        msg = self._conn.spop(queue)
        return deserialize(msg) if msg else msg

    def pushleft(self, queue, msg):
        self._conn.lpush(queue, serialize(msg))

    def llen(self,k):
        return self._conn.llen(k)

    def keys(self, pattern="*"):
        return self._conn.keys(pattern)

redis_conn = MessageQueue(REDIS_HOST,REDIS_PORT)._conn
rq_conn = Queue(connection=redis_conn)
fetch = Job.fetch

if __name__ == "__main__":
    job_id = 'rq:job:d65aade8-5304-48d3-8477-9ac16f7cefd8'
    job_id = job_id.split(':')[2] 
    res = fetch(job_id.decode("utf-8", "ignore"),redis_conn)
    print res.to_dict()
