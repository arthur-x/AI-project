# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

file1 = 'out.txt'
file2 = 'in.txt'
df = pd.DataFrame(data = None)

with open(file1, 'r') as OUT:   
    while True:
        state = []
        dic = {}
        OUT.seek(0,0)
        line = OUT.readline() 
        if not line:
            break
        line = line.strip()
        state = [i for i in line.split(',')]
        for seg in state[1:]:
            i,j = seg.split('=')
            dic[i] = float(j)
        dic = pd.DataFrame(dic,index=[0])
        #The output order is in:
        #aileron,elevator,rudder,throttle0,throttle1 
        output = np.random.uniform(-1,1,size=(5))
        with open(file2, 'w') as IN: 
            for item in range(4):
                IN.write(str(output[item])+',')
            IN.write(str(output[4]))

