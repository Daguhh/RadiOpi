#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:25:04 2017

@author: david
"""

class MonException(Exception):
    def __init__(self,raison):
        self.raison = raison
    def __str__(self):
        return self.raison


def multiplier_par_5(n):
    if n > 20:
        raise MonException("Le nombre est trop grand !")
    else:
        return n * 5
a= 10
try:
    print(multiplier_par_5(2))
    print(multiplier_par_5(21))
    a=a*2
except MonException as e:
    print(e)
    
print(a)