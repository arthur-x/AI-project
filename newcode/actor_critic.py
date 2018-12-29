# -*- coding: utf-8 -*-
import torch.nn as nn
import torch


class Actor(nn.Module):
    def __init__(self):
        super(Actor, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(31, 200),
            nn.ReLU(),
            nn.Linear(200, 100),
            nn.ReLU(),
            nn.Linear(100, 5),
            nn.Tanh())

    def forward(self, x):
        output = self.layer1(x)
        return output


class Policy:
    def __init__(self, actor, scaler):
        self.actor = actor
        self.scaler = scaler

    def act(self, state):
        state = self.scaler.transform(state)
        state = torch.from_numpy(state)
        state = torch.tensor(state, dtype=torch.float)
        action = self.actor(state)
        action = action.detach().numpy()
        return action


class Critic(nn.Module):
    def __init__(self):
        super(Critic, self).__init__()
        self.layer1 = nn.Sequential(
                nn.Linear(31, 200),
                nn.ReLU(),
                nn.Linear(200, 100),
                nn.ReLU(),
                nn.Linear(100, 1))
 
    def forward(self, x):
        output = self.layer1(x)
        return output  
