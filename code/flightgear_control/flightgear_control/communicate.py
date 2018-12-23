# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import pickle
from angle import angle

'''construct net'''
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.layer1 = nn.Sequential(
                nn.Linear(26, 400),
                nn.ReLU(),
                nn.Linear(400, 300),
                nn.ReLU(),
                nn.Linear(300, 5),
                nn.Tanh())
 
    def forward(self, x):
        output = self.layer1(x)
        #print(output)
        return output  
    
file1 = 'out.txt'
file2 = 'in.txt'
df = pd.DataFrame(data = None)

FILENAME = 'scalers.pickle'
with open(FILENAME, 'rb') as f:
    scaler1= pickle.load(f)

net = torch.load('nn.pkl')

'''departure: Hawaii'''
'''destination: San Francisco'''
target_latitude = 37.7
target_longitude = -122.4
target_altitude = 5000

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
        df = pd.DataFrame(dic,index=[0])
        fea = df[['ai-offset','ai-pitch','ai-roll','airspeed-kt',
                 'alt-ft','altitude','down-accel-fps_sec','east-accel-fps_sec',
                 'flaps','heading-deg','hi-heading','latitude',
                 'longitude','north-accel-fps_sec','pitch-deg','roll-deg',
                 'speed-down-fps','speed-east-fps','speed-north-fps',
                 'uBody-fps','vBody-fps',
                 'vsi-fpm','wBody-fps','x-accel-fps_sec','y-accel-fps_sec',
                 'z-accel-fps_sec']]
        target_heading = angle(dic['longitude'],dic['latitude'],target_longitude,target_latitude)
        heading_error = dic['heading-deg'] - target_heading
        if heading_error > 180:
            heading_error -= 360    
        if heading_error < -180:
            heading_error += 360
        height_error = dic['altitude'] - target_altitude
        #print(heading_error,height_error)
        
        #The output order is in:
        #aileron,elevator,rudder,throttle0,throttle1 
        #output = np.random.uniform(-1,1,size=(5))
        sample = fea.values
        sample = scaler1.transform(sample)
        sample = torch.from_numpy(sample)
        sample = torch.tensor(sample,dtype = torch.float)
    
        output = net(sample)
        
        output = output.detach().numpy()
        with open(file2, 'w') as IN:
            IN.write(str(output[0,0])+',')
            IN.write(str(output[0,1])+',')
            IN.write(str(output[0,2])+',')
            IN.write(str(output[0,3])+',')
            IN.write(str(output[0,4]))
        