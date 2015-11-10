from tornado import (
    gen,
    ioloop,
    log,
    web
)

from .handlers import _AsyncBase, _Base, _ThreadPoolBase, _MessageQueueBase

class RPCServer(object):

    def __init__(self):
        self._routes = []
        self.log = log.logging.getLogger()
        self.log.setLevel(log.logging.INFO)
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
#        app.listen(int(port),host)
#        ioloop.IOLoop.current().start()

        from tornado.httpserver import HTTPServer 
        server = HTTPServer(web.Application(self._routes, debug=True),xheaders=True) 
        server.listen(port, host)
        ioloop.IOLoop.current().start()

__all__ = ('RPCServer')
