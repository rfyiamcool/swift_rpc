#coding:utf-8
from tornado import (
    gen,
    ioloop,
    log,
    web
)

from tornado.httpserver import HTTPServer 
from .handlers import _AsyncBase, _Base, _ThreadPoolBase, _MessageQueueBase
from swift_rpc.log import get_logger

class RPCServer(object):

    def __init__(self,logfile=None):
        self._routes = []
        if logfile:
            self.log = get_logger(logfile)
        else:
            self.log = log.logging.getLogger()
        log.enable_pretty_logging(logger=self.log)
        self.register_async(self._getroutes)

    @gen.coroutine
    def _getroutes(self):
        raise gen.Return([v.__name__ for _, v in self._routes])

    def _make(self, func, base):
        name = func.__name__
        handler = type(name, (base,), {'func': [func]})
        self._routes.append((r'/{0}'.format(name), handler))
        self.log.info('Registered {0} command {1}'.format(base.TYPE, name))

    def register(self, func):
        self._make(func, _Base)

    def register_async(self, func):
        self._make(func, _AsyncBase)

    def register_pool(self, func):
        self._make(func, _ThreadPoolBase)

    def register_mq(self, func):
        self._make(func, _MessageQueueBase)

    def start(self, host, port):
        self.log.info('Starting server on port {0}'.format(port))
#        app = web.Application(self._routes, debug=True)
        server = HTTPServer(web.Application(self._routes, debug=True),xheaders=True) 
        server.listen(int(port), host)
        ioloop.IOLoop.current().start()

__all__ = ('RPCServer')

if __name__ == "__main__":
    pass
