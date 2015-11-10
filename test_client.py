from swift_rpc.client import RPCClient

client = RPCClient('localhost:8080')
print client.test('hi')
print client.test_async('hi')
