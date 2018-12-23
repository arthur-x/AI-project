# -*- coding: utf-8 -*-
import numpy as np

output = np.zeros((1,5))
file2 = 'in.txt'

with open(file2, 'w') as IN:
    for item in range(4):
        IN.write(str(output[0,item])+',')
    IN.write(str(output[0,4]))
