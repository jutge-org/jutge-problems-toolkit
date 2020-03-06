#!/usr/bin/python
# -*- coding: latin1 -*-

from random import *

for x in range(100):
    for i in range(10):
        print i
        for j in range(i):
            if randint(0, 100)>20:
                print "%2.2f" % uniform(0, 10), randint(0, 1)
            else:
                print -1, randint(0, 1)
        print

