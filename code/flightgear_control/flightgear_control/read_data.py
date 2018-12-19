# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

filename = 'test.txt'
df = pd.DataFrame(data = None)

with open(filename, 'r') as f:
    while True:
        state = []
        dic = {}
        line = f.readline() 
        if not line:
            break
        line = line.strip()
        state = [i for i in line.split(',')]
        for seg in state[1:]:
            i,j = seg.split('=')
            dic[i] = float(j)
        dic = pd.DataFrame(dic,index=[0])
        df = pd.concat([df,dic])
        
df.to_csv('data.csv', columns=df.columns, index=False)

