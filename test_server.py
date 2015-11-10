#coding:utf-8
import time
from tornado import gen
from swift_rpc.server import RPCServer
from config import *
from api import *

def test(args,**kwargs):
    return "You said %s" % args

def test_block(args):
    time.sleep(5)
    return "You said "

@gen.coroutine
def test_async(arg):
    raise gen.Return("You said async %s" % arg)


if __name__ == "__main__":
    server = RPCServer()
    server.register(test)
    server.register_async(test_async)
    server.register_pool(test_block)
    server.register_mq(test_mq)
    server.register_mq(go)
    server.start(RPC_HOST,RPC_PORT)
