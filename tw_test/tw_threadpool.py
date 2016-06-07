#!/usr/local/bin/python

from twisted.internet import reactor

def aSillyBlockingMethod(x):
    import time
    time.sleep(2)
    print(x)

reactor.callInThread(aSillyBlockingMethod, "2 seconds have passed")
reactor.run()

