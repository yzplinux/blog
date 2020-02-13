#!/usr/bin/env python 
# -*- coding:utf-8 -

class tmp(object):
    a = 1
    b = 2
    c = 3

    def abc(self):
        return self.a,self.b

print(tmp().abc())