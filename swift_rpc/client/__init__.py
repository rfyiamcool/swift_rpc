import json
import base64
import requests
from urlparse import urljoin

class _RPC(object):

     def __init__(self, server, name, encryption):
        self.encryption = encryption
        self.__HEADERS__ = {'User-Agent': 'swift_rpc','Content-Type':'application/json'}
        if encryption:
            self.__HEADERS__ = {'User-Agent': 'swift_rpc','Content-Type':'application/json','Encryption':encryption}
        
        self._name = name
        self._url = urljoin(server, name)
    
     def __call__(self, *args, **kwargs):
        params = {}
        params['args'] = args
        params['kwargs'] = kwargs
        post_data = json.dumps(params)
        if self.encryption:
            post_data = base64.encodestring(post_data)
        try:
            resp = requests.get(self._url, data=post_data, headers=self.__HEADERS__)
        except Exception as e:
            raise RPCClient.FailedCall(e)
    
        if resp.status_code == 404:
            raise RPCClient.MissingMethod(
              'No remote method found for {0}'.format(self._name))
    
        try:
            ret = json.loads(resp.content)
        except Exception as e:
            raise RPCClient.InvalidSerializationError(e)
    
        if 'error' in ret:
            raise RPCClient.FailedCall(ret['error'])
    
        return ret['response']
    
class RPCClient(object):

    class FailedCall(Exception): pass
    class InvalidSerializationError(Exception): pass
    class MissingMethod(Exception): pass

    __UNALLOWED__ = [
        'trait_names',
        '_getAttributeNames',
    ]

    def __init__(self, server,encryption=None, unallowed_calls=[], load_remotes=True):
        self.encryption = encryption
        if server.startswith('http'):
            self._server = server
        else:
            self._server = 'http://{0}'.format(server)
        self._unallowed = unallowed_calls + self.__UNALLOWED__
        if load_remotes:
            self.__loadremoteroutes()

    def __send(self, name):
        return _RPC(self._server, name, self.encryption)

    def __remoteroutes(self):
        return self._getroutes()

    def __loadremoteroutes(self):
        for route in self.__remoteroutes():
            setattr(self, route, self.__send(route))

    def __getattr__(self, name):
        return None if name in self._unallowed else self.__send(name)


__all__ = ('RPCClient')
