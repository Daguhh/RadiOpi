#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:22:54 2017

@author: david
"""
import numpy as np
from matplotlib import pyplot as plt
g=-1
x0=30
v0=0
x=np.zeros(100)
t = np.arange(100)
i=0
for j in t :
    x[j] = g*i**2/2+v0*i+x0
    v_t = g*i
    print(v_t)
    if x[j] < 0 :
        if x[j-1]>=0 :
            print("============")
            v0 = -(v_t+v0)*0.7
            print(v0)
            i=0
            x0=0
    i+=0.5
#x=np.round(x/np.max(x)*31)    
plt.plot(t,x)
plt.show() 