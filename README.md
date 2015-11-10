# swift_rpc

swift_rpc是用tornado实现的rpc服务,现在开放了四个调度接口:  

1. register 普通接口调用模式,最纯粹最简单  
2. register_async 借助于tornado gen.coroutine实现的非堵塞调用  
3. register_pool  借助于futures.ThreadPoolExecutor实现线程池  
4. register_mq 通过mq异步调用方法，适合后端长时间运算或耗时的调用

Tornado RPC Server Usage:

```
#coding:utf-8
import time
from tornado import gen
from swift_rpc.server import RPCServer
from config import *


def test(args,**kwargs):
    return "You said %s" % args

def test_block(args):
    time.sleep(5)
    return "You said "

@gen.coroutine
def test_async(arg):
    raise gen.Return("You said async %s" % arg)

def test_mq(arg):
    print 'mq...'
    return "You said "

server = RPCServer()
server.register(test)
server.register_async(test_async)
server.register_pool(test_block)
server.register_mq(test_mq)
server.start(RPC_HOST,RPC_PORT)
```

swift_rpc client Usage:

```
#coding:utf-8
import time
from tornado import gen
from swift_rpc.server import RPCServer
from config import *


def test(args,**kwargs):
    return "You said %s" % args

def test_block(args):
    time.sleep(5)
    return "You said "

@gen.coroutine
def test_async(arg):
    raise gen.Return("You said async %s" % arg)

def test_mq(arg):
    print 'mq...'
    return "You said "

server = RPCServer()
server.register(test)
server.register_async(test_async)
server.register_pool(test_block)
server.register_mq(test_mq)
server.start(RPC_HOST,RPC_PORT)
```
