#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8") 

import time
from tornado import gen
from swift_rpc.server import RPCServer
from swift_rpc.mq import rq_conn
from swift_rpc.mq import redis_conn
from swift_rpc.mq import fetch
from config import *
import config
from api import *

def test(args):
    return "this is test %s"%(args)

def test_args(a,b,name='xiaorui.cc'):
    print a,b,name
    return "this is test %s %s"%(a,name)

def get_result(job_id):
    return redis_conn.hgetall(job_id)

def test_block(args):
    time.sleep(5)
    return "You said "

@gen.coroutine
def test_async(arg):
    return gen.Return("this is test_async async %s" % arg)

if __name__ == "__main__":
    server = RPCServer(config)
    server.register(test)
    server.register(test_args)
    server.register(get_result)
    server.register_async(test_async)
    server.register_pool(test_block)
    server.register_mq(test_mq)
    server.register_mq(go)
    server.start(RPC_HOST,RPC_PORT)
