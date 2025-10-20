#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Last modified on Mon Sep 29 13:06 2025 

@author: oliver
"""
import numpy as np
from minirace import Minirace

therace = Minirace(level=1)

# create big enough dataset
rows = therace.xymax * therace.xymax * 5
columns = therace.xymax * therace.xymax + 1

alldata = np.zeros((rows, columns), dtype=int)

for i in range(rows):
    therace.reset()
    for j in range(2):
        x, z, _ = therace.s1
        if abs(z[2] - x) <= 1.0:
            therace.transition()
    
    x, z, _ = therace.s1
    alldata[i,:-1] = therace.to_pix(x, z).flatten()
    
    if (abs(z[2] - x) <= 1.0):
        alldata[i,-1] = 1.0
    else:
        alldata[i,-1] = 0.0
        
# save all pictures and all labels in random order, two separate files            
np.random.seed(10)
neworder = np.random.choice(rows, size=rows, replace=False)
alldata = alldata[neworder,:]
np.savetxt('alldata.csv', alldata, delimiter=',', fmt='%d')

# number of training and test samples
ntrain = round(0.8 * rows)
ntest = rows - ntrain

trainingdata = alldata[0:ntrain,:]
testingdata = alldata[ntrain:,:]

np.savetxt('trainingpix.csv', trainingdata, delimiter=',', fmt='%d')
np.savetxt('testingpix.csv', testingdata, delimiter=',', fmt='%d')
