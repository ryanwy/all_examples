#!/usr/local/bin/python

import multiprocessing
import time

def f():
    i = 0
    while i < 10000:
        print "running:" + str(i)
        time.sleep(1)
        i += 1
def create_process():
    p = multiprocessing.Process(target = f, name = "mytest")
    p.start()
    print p.pid
    p.join()

def create_process_pool():
    try:
        pool = multiprocessing.Pool(5)
        res = pool.apply_async(f)
        print res.get()
    except Exception as e:
        print e
if __name__ == "__main__":
    #create_process()
    create_process_pool()
