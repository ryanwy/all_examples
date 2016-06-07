#!/usr/local/bin/python

#from test_module import func
try:
    from test_module.test_module  import module1
    from test_module2 import module2
except ImportError as e:
    print e

if __name__ == "__main__":
    m1 = module1()
    m1.func()
    m2 = module2()
    m2.func()
