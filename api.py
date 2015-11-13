#coding:utf-8
import time
def go(*args,**kwargs):
    print 'this go func in MQ'
    return "You said "

def test_mq(*args,**kwargs):
    time.sleep(10)
    print 'mq...'
    return "You said "

__all__ = ('go','test_mq')
