#!/usr/bin/env python
# coding: utf-8

import os
from twisted.internet import defer, reactor, utils
from twisted.internet.defer import inlineCallbacks

@inlineCallbacks
def ls_file(i):
    d = yield utils.getProcessOutput("/bin/ls", ["-l","/tmp/test.file" + str(i)], env=os.environ)
    defer.returnValue(d)

@inlineCallbacks
def ls_list(count):
    d_list = yield defer.DeferredList([touch_file(i) for i in xrange(count)])
    defer.returnValue(d_list)

def sort_result(defer_list):
    results = [result for status, result in defer_list if status]
    results.sort()
    print results

def main():
    d_list = ls_list(20)
    d_list.addCallback(sort_result)
    d_list.addCallback(lambda s:reactor.stop())
    reactor.run()

if __name__ == "__main__":
    main()
