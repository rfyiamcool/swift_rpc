#coding:utf-8
def go(*args,**kwargs):
    print 'this go func in MQ'
    return "You said "

def test_mq(*args,**kwargs):
    print 'mq...'
    return "You said "

__all__ = ('go','test_mq')
