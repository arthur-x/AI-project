# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import pickle
from angle import angle
import math


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
    

'''departure: Hawaii'''
'''destination: San Francisco'''
def reward(dic):
    target_latitude = 37.7
    target_longitude = -122.4
    target_altitude = 5000
    target_heading = angle(dic['longitude'],dic['latitude'],target_longitude,target_latitude)
    '''
    heading_error = dic['heading-deg'] - target_heading
    if heading_error > 180:
        heading_error -= 360    
    if heading_error < -180:
        heading_error += 360
    '''
    height_error = abs(dic['altitude'] - target_altitude)
    #creating vector to calculate speed error
    target_vector = np.array([math.cos(2*target_heading*math.pi/360),math.sin(2*target_heading*math.pi/360),0])
    current_vector = np.array([dic['speed-north-fps'],dic['speed-east-fps'],dic['speed-down-fps']])
    #print(target_vector,current_vector)
    COS = (target_vector.dot(current_vector))/(np.linalg.norm(target_vector)*np.linalg.norm(current_vector))
    
    reward = COS/2 + math.exp(-height_error*0.0005)-1/2
    
    return reward


class env:
    def __init__(self,output_file,input_file):
        self.input_file = input_file
        self.output_file = output_file
        self.baseline = 4802
        #this is a little bit larger than 4800 in order to counter delays
        
    def reset(self):
        '''wait for the environment to return to the start state'''
        with open(self.output_file, 'r') as OUT:  
            while True:
                state = []
                dic = {}
                OUT.seek(0,0)
                line = OUT.readline() 
                line = line.strip()
                state = [i for i in line.split(',')]
                for seg in state[1:]:
                    i,j = seg.split('=')
                    dic[i] = float(j)
                if dic['altitude']>self.baseline:
                    break
            
            df = pd.DataFrame(dic,index=[0])
            fea = df[['ai-offset','ai-pitch','ai-roll','airspeed-kt',
                     'alt-ft','altitude','down-accel-fps_sec','east-accel-fps_sec',
                     'flaps','heading-deg','hi-heading','latitude',
                     'longitude','north-accel-fps_sec','pitch-deg','roll-deg',
                     'speed-down-fps','speed-east-fps','speed-north-fps',
                     'uBody-fps','vBody-fps',
                     'vsi-fpm','wBody-fps','x-accel-fps_sec','y-accel-fps_sec',
                     'z-accel-fps_sec']]
            s = fea.values
            return s
        
    def step(self,action):
        '''action is a numpy array with shape(1,5)'''
        #The order is:
        #aileron,elevator,rudder,throttle0,throttle1 
        with open(self.input_file, 'w') as IN:
            IN.write(str(action[0,0])+',')
            IN.write(str(action[0,1])+',')
            IN.write(str(action[0,2])+',')
            IN.write(str(action[0,3])+',')
            IN.write(str(action[0,4]))
            
        with open(self.output_file, 'r') as OUT:   
            state = []
            dic = {}
            OUT.seek(0,0)
            line = OUT.readline() 
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
            
            '''reward is in -1 to +1'''
            r = reward(dic)        
            '''s(state) is a numpy array with shape(1,26)'''
            s = fea.values
            done = dic['altitude']<self.baseline
            
        return s, r, done


class policy:
    def __init__(self,net,scaler):
        self.net = net
        self.scaler = scaler
        
    def act(self,state):
        state = self.scaler.transform(state)
        state = torch.from_numpy(state)
        state = torch.tensor(state,dtype = torch.float)
        action = self.net(state)
        action = action.detach().numpy()
        return action


if __name__ == '__main__':
    
    file1 = 'out.txt'
    file2 = 'in.txt'
    with open('scalers.pickle', 'rb') as f:
        scaler1= pickle.load(f)
    net = torch.load('nn.pkl')
    
    P = policy(net,scaler1)
    fg = env(file1,file2)
    
    N_episode = 10
    
    for i in range(N_episode):
        s = fg.reset()
        while True:      
            '''take action'''
            a = P.act(s)
            '''get observation & reward'''
            s,r,done = fg.step(a)
            if done:break
