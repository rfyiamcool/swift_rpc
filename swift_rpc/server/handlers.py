#coding:utf-8
import json
from tornado import gen, log, web
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from swift_rpc.mq import rq_conn,redis_conn

class _Handler(web.RequestHandler):
    __ALLOWEDUA__ = ('swift_rpc')

    @gen.coroutine
    def initialize(self):
        self.log = log.logging.getLogger()
        self.log.setLevel(log.logging.INFO)

    @gen.coroutine
    def prepare(self):
        if self.config.SAFE_UA_MODE:
            ua = self.request.headers.get('User-Agent')
            #if ua not in self.__ALLOWEDUA__:
            if ua not in self.config.UA_ALLOW:
                self.log.info('Received request from UA {0}'.format(ua))
                self.write({'error': 'User agent not allowed: {0}'.format(ua)})
                self.finish()

        if self.config.SAFE_TOKEN_MODE:
            token = self.request.headers.get('Token')
            if token not in self.TOKEN_ALLOW:
                self.log.info('Received request from Token {0}'.format(token))
                self.write({'error': 'Token not allowed: {0}'.format(token)})
                self.finish()

        if self.config.REMOTE_IP_MODE:
            remote_ip = self.request.headers.get("X-Real-IP")
            remote_ip = remote_ip if remote_ip else self.request.remote_ip
            if remote_ip not in self.config.REMOTE_ALLOW:
                self.log.info('Received request from REMOTE IP {0}'.format(remote_ip))
                self.write({'error': 'IP not allowed: {0}'.format(remote_ip)})
                self.finish()

    @gen.coroutine
    def args_kwargs(self):
        args = []
      # support positional arguments
        if self.request.headers.get('Content-Type') == "application/json":
            data = json.loads(self.request.body)
            args = data.get('args',[])
            kwargs = data.get('kwargs',{})
            raise gen.Return((args, kwargs))

        if 'args' in self.request.arguments:
            args = self.request.arguments['args']
            del self.request.arguments['args']
        kwargs = dict([(k, v[0]) for k, v in self.request.arguments.items()])
        raise gen.Return((args, kwargs))

class _Base(_Handler):

    TYPE = 'synchronous'

    @gen.coroutine
    def get(self):
        args, kwargs = yield self.args_kwargs()
        try:
            self.write({'response': self.func[0](*args, **kwargs)})
        except Exception as e:
            self.write({'error': str(e)})

class _AsyncBase(_Handler):
    TYPE = 'asynchronous'

    @gen.coroutine
    def get(self):
        args, kwargs = yield self.args_kwargs()
        try:
            ret = yield self.func[0](*args, **kwargs)
      # return JSON so we get the correct type of the return value
            self.write({'response': ret})
        except Exception as e:
            self.write({'error': str(e)})

class _ThreadPoolBase(_Handler):
    executor = ThreadPoolExecutor(200)
    TYPE = 'threadpool'

    @gen.coroutine
    def get(self):
        args, kwargs = yield self.args_kwargs()
        try:
            data = yield self.run(self.func,args,kwargs)
            self.write({'response': data})
        except Exception as e:
            self.write({'error': str(e)+"aa"})

    @run_on_executor
    def run(self,func,args,kwargs):
        return self.func[0](*args, **kwargs)

class _MessageQueueBase(_Handler):
    TYPE = 'mqasync'

    @gen.coroutine
    def get(self):
        args, kwargs = yield self.args_kwargs()
        try:
            job = rq_conn.enqueue('api.'+self.func[0].func_name,*args,**kwargs)
            """
            will fix better
#           r.lpush('task',msgpack.packb([self.func[0].func_name,args,kwargs]))
            """
            self.write({'response': 'commit','job':job.key})
        except Exception as e:
            self.write({'error': str(e)})

if __name__ == "__main__":
    pass
