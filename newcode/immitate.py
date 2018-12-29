# -*- coding: utf-8 -*-
import numpy as np
import torch
import torch.nn as nn
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pickle
from actor_critic import Actor, Policy


def load_data(filename):
    file = pd.read_csv(filename)

    fea = file[['ai-offset', 'ai-pitch', 'ai-roll', 'airspeed-kt',
                'alt-ft', 'altitude', 'down-accel-fps_sec', 'east-accel-fps_sec',
                'flaps', 'heading-deg', 'hi-heading', 'latitude',
                'longitude', 'north-accel-fps_sec', 'pitch-deg', 'roll-deg',
                'speed-down-fps', 'speed-east-fps', 'speed-north-fps',
                'uBody-fps', 'vBody-fps',
                'vsi-fpm', 'wBody-fps', 'x-accel-fps_sec', 'y-accel-fps_sec',
                'z-accel-fps_sec', 'aileron', 'elevator', 'rudder', 'throttle0', 'throttle1']]

    act = file[['aileron', 'elevator', 'rudder', 'throttle0', 'throttle1']]

    delay = 1
    act = act.shift(-1 * delay)  # account for delay
    for i in range(delay):
        fea = fea.drop([fea.last_valid_index()])
    act.dropna(inplace=True)

    x = np.array(fea)
    y = np.array(act)

    scaler = StandardScaler().fit(x)
    standardized_features = scaler.transform(x)

    labels = y

    x_train, x_test, y_train, y_test = train_test_split(standardized_features, labels, test_size=0.01, random_state=0)

    x_train = torch.from_numpy(x_train)
    x_train = torch.tensor(x_train, dtype=torch.float)

    x_test = torch.from_numpy(x_test)
    x_test = torch.tensor(x_test, dtype=torch.float)

    y_train = torch.from_numpy(y_train)
    y_train = torch.tensor(y_train, dtype=torch.float)

    y_test = torch.from_numpy(y_test)
    y_test = torch.tensor(y_test, dtype=torch.float)

    return x_train, x_test, y_train, y_test, scaler


def valid_train(net, loss_func, train_set_samples, train_set_labels):
    y_pred = net(train_set_samples[:500, :])
    train_loss = float(loss_func(y_pred, train_set_labels[:500, :]))
    return train_loss


def valid_test(net, loss_func, test_set_samples, test_set_labels):
    y_pred = net(test_set_samples)
    test_loss = float(loss_func(y_pred, test_set_labels))
    return test_loss


def main():
    train_set_samples, test_set_samples, train_set_labels, test_set_labels, scaler = load_data('data.csv')

    loss_func = nn.MSELoss()

    # training model from zero
    batchsize = 30
    batches = int(train_set_samples.shape[0] / batchsize)
    epoch = 100

    net = Actor()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)

    train_loss_trace = []
    test_loss_trace = []

    # begin training
    for i in range(epoch):
        net.train()
        for j in range(batches):
            samples = train_set_samples[j * batchsize:(j + 1) * batchsize, :]
            labels = train_set_labels[j * batchsize:(j + 1) * batchsize, :]
            optimizer.zero_grad()
            y_pred = net(samples)
            loss = loss_func(y_pred, labels)
            loss.backward()
            optimizer.step()

        net.eval()
        # test on train samples
        train_loss = valid_train(net, loss_func, train_set_samples, train_set_labels)
        train_loss_trace.append(train_loss)
        print('epoch:', i + 1, ',train_loss:', train_loss)
        # test on test samples
        test_loss = valid_test(net, loss_func, test_set_samples, test_set_labels)
        print('epoch:', i + 1, ',test_loss:', test_loss)
        test_loss_trace.append(test_loss)

    plt.plot(train_loss_trace, label='train_loss')
    plt.plot(test_loss_trace, label='test_loss')
    plt.xlabel('epoch')
    plt.legend()
    plt.show()
    policy = Policy(net, scaler)
    with open('policy.pkl', 'wb') as file:
        pickle.dump(policy, file)


if __name__ == '__main__':
    main()
