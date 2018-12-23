# -*- coding: utf-8 -*-
import numpy as np
import torch
import torch.nn as nn
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split 
import matplotlib.pyplot as plt
import pickle

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
    
    
def loadData(filename):
    file = pd.read_csv(filename)

    fea = file[['ai-offset','ai-pitch','ai-roll','airspeed-kt',
                 'alt-ft','altitude','down-accel-fps_sec','east-accel-fps_sec',
                 'flaps','heading-deg','hi-heading','latitude',
                 'longitude','north-accel-fps_sec','pitch-deg','roll-deg',
                 'speed-down-fps','speed-east-fps','speed-north-fps',
                 'uBody-fps','vBody-fps',
                 'vsi-fpm','wBody-fps','x-accel-fps_sec','y-accel-fps_sec',
                 'z-accel-fps_sec']]
    
    act = file[['aileron','elevator','rudder','throttle0','throttle1']]
    
    delay = 3
    act = act.shift(-1*delay)# account for delay
    for i in range(delay):
        fea = fea.drop([fea.last_valid_index()])
    act.dropna(inplace=True)

    x = np.array(fea)
    y = np.array(act)
    
    scaler1 = StandardScaler().fit(x)
    standardized_features = scaler1.transform(x) 
    #scaler2 = StandardScaler().fit(y)
    #labels = scaler2.transform(y) 
    labels = y
    #print(labels[:5,:])
   
    X_train, X_test, y_train, y_test = train_test_split(standardized_features,labels,test_size=0.01,random_state = 0)
    
    X_train = torch.from_numpy(X_train)
    X_train = torch.tensor(X_train,dtype = torch.float)
    
    X_test = torch.from_numpy(X_test)
    X_test = torch.tensor(X_test,dtype = torch.float)
    
    y_train = torch.from_numpy(y_train)
    y_train = torch.tensor(y_train,dtype = torch.float)
    
    y_test = torch.from_numpy(y_test)
    y_test = torch.tensor(y_test,dtype = torch.float)
    #print(X_train[:5,:])
    return X_train, X_test, y_train, y_test, scaler1#, scaler2
 
    
def valid_train(net,loss_func,train_set_samples,train_set_labels):
    y_pred = net(train_set_samples[:500,:])
    train_loss = float(loss_func(y_pred,train_set_labels[:500,:]))
    return train_loss
    

def valid_test(net,loss_func,test_set_samples,test_set_labels):
    y_pred = net(test_set_samples)
    test_loss = float(loss_func(y_pred,test_set_labels))
    return test_loss


def main():
    train_set_samples,test_set_samples,train_set_labels,test_set_labels,scaler1=loadData('data.csv')
    #print(train_set_samples.shape,test_set_samples.shape,train_set_labels.shape,test_set_labels.shape)
    #print(train_set_samples[:5,:])
    FILENAME = 'scalers.pickle'
    with open(FILENAME, 'wb') as f:
        pickle.dump(scaler1,f)
        
    loss_func = nn.MSELoss()
    '''
    #load trained model
    net = torch.load('nn.pkl')

    net.eval()
    correct_count = 0
    loss_count = 0
    for k in range(20):
        y_pred = net(test_set_samples[k*500:(k+1)*500,:,:,:])
        correct = (torch.argmax(y_pred,1) == test_set_labels[k*500:(k+1)*500])
        correct_count += int(correct.sum())
        loss_count += float(loss_func(y_pred,test_set_labels[k*500:(k+1)*500]))
    test_loss = loss_count/20
    test_accuracy = correct_count/10000
    print('due to randomness, each run result may not be the same.')
    print('model test set accuracy:',test_accuracy,'model test set loss:',test_loss)
    correct_count = 0
    loss_count = 0
    for k in range(120):
        y_pred = net(train_set_samples[k*500:(k+1)*500,:,:,:])
        correct = (torch.argmax(y_pred,1) == train_set_labels[k*500:(k+1)*500])
        correct_count += int(correct.sum())
        loss_count += float(loss_func(y_pred,train_set_labels[k*500:(k+1)*500]))
    train_loss = loss_count/120
    train_accuracy = correct_count/60000
    print('model train set accuracy:',train_accuracy,'model train set loss:',train_loss)
    
    '''
    #training model from zero
    batchsize = 30
    batches = int(train_set_samples.shape[0]/batchsize)
    epoch = 100
    
    net = Net()
    optimizer = torch.optim.Adam(net.parameters(),lr = 0.001)
    
    train_loss_trace = []
    test_loss_trace = []

    #begin training
    for i in range(epoch):
        net.train()
        for j in range(batches):
            samples = train_set_samples[j*batchsize:(j+1)*batchsize,:]
            labels = train_set_labels[j*batchsize:(j+1)*batchsize,:] 
            #print(samples[:5,:])
            #print(labels[:5,:])
            optimizer.zero_grad()
            y_pred = net(samples)
            loss = loss_func(y_pred,labels)
            #print(y_pred)
            loss.backward()
            optimizer.step()
            
            
        net.eval()
        #test on train samples 
        train_loss = valid_train(net,loss_func,train_set_samples,train_set_labels)
        train_loss_trace.append(train_loss)
        print('epoch:',i+1,',train_loss:',train_loss)
        #test on test samples 
        test_loss = valid_test(net,loss_func,test_set_samples,test_set_labels)
        print('epoch:',i+1,',test_loss:',test_loss)
        test_loss_trace.append(test_loss)
    
    plt.plot(train_loss_trace,label = 'train_loss')   
    plt.plot(test_loss_trace,label = 'test_loss')
    plt.xlabel('epoch')
    plt.legend()
    plt.show()
    torch.save(net,'nn.pkl')
    
    
if __name__ == '__main__':
    main()

