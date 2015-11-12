# swift_rpc

swift_rpc是用tornado实现的rpc服务,现在开放了四个调度接口:  

[更多的关于swift的开发信息](http://xiaorui.cc)

1. register 普通接口调用模式,最纯粹最简单    
2. register_async 借助于tornado gen.coroutine实现的非堵塞调用  
3. register_pool  借助于futures.ThreadPoolExecutor实现线程池  
4. register_mq 通过mq异步调用方法，适合后端长时间运算或耗时的调用

Change Log:  

Version: 2.1  
1. 解决Nginx针对RPC负载均衡时，无法正常获取remote_ip

Version: 2.2  
1. rq enqueue塞入任务队列时的一个bug,已经绕过解决

Version: 2.3  
1. 解决了curl调用rq的get_result时出现的0x80 code异常

Version: 2.4  
1. 日志及加密模式

Future:  
1. 统一配置配置文件  
2. 使用rsa保证rpc通信安全 
3. swift_rpc完善RQ异步任务队列  
4. 增加request json body的识别,在这基础上做安全的封装


测试json body的args,kwargs:  
```
curl -H "Content-Type: application/json" -H "User-Agent: swift_rpc" -X GET -d '{"args":"[123,456]","kwargs":{"name":1}}' http://localhost:8080/test_args
curl -H "Content-Type: application/json" -H "User-Agent: swift_rpc" -X GET -d '{"args":"123"}' http://localhost:8080/test
```

测试选择加密模式:  
```
curl -H "Encryption: base64" -H "Content-Type: application/json" -H "User-Agent: swift_rpc" -X GET -d '{"args": [123, 456], "kwargs": {"name": 1}}'  http://localhost:8080/test_args
```

测试arguments的args,kwargs:  
```
curl -H "User-Agent: swift_rpc" -X GET -d "args=123" http://localhost:8080/test
```

Tornado RPC Server Usage:

```
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
    server = RPCServer()
    server.register(test)
    server.register(test_args)
    server.register(get_result)
    server.register_async(test_async)
    server.register_pool(test_block)
    server.register_mq(test_mq)
    server.register_mq(go)
    server.start(RPC_HOST,RPC_PORT)
```

swift_rpc client Usage:

```
from swift_rpc.client import RPCClient

client = RPCClient('localhost:8080')
print client.test('hi')
print client.test_args('welcome','xiaorui.cc',name='nima')
```


