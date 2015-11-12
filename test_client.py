from swift_rpc.client import RPCClient

client = RPCClient('localhost:8080',encryption='base64')
print client.test('hi')
print client.test_args('welcome','xiaorui.cc',name='nima')
