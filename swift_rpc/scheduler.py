#coding:utf-8
from Queue import Queue
from serialize import serialize, deserialize
from config import *
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

q = Queue()
r = MessageQueue(REDIS_HOST,REDIS_PORT)._conn
