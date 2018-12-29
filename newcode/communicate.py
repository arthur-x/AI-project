# -*- coding: utf-8 -*-
import pickle
from env import Env


if __name__ == '__main__':
    print("client begin!")
    input("press enter to continue!")

    with open('policy.pkl', 'rb') as f:
        P = pickle.load(f)

    n_episode = 10
    fg = Env()

    for i in range(n_episode):
        s = fg.reset()
        while True:
            '''take action'''
            a = P.act(s)
            '''get observation & reward'''
            s, r, done = fg.step(a)
            if done:
                print('episode', i+1, '/', n_episode, 'ended!')
                break
