# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd
import socket
from client import pid, receiver
from angle import angle


'''departure: Hawaii'''
'''destination: San Francisco'''


def reward(dic):
    target_latitude = 37.7
    target_longitude = -122.4
    target_altitude = 5000
    target_heading = angle(dic['longitude'], dic['latitude'], target_longitude, target_latitude)
    height_error = abs(dic['altitude'] - target_altitude)
    # creating vector to calculate speed error
    target_vector = np.array(
        [math.cos(2 * target_heading * math.pi / 360), math.sin(2 * target_heading * math.pi / 360), 0])
    current_vector = np.array([dic['speed-north-fps'], dic['speed-east-fps'], dic['speed-down-fps']])
    projection = (target_vector.dot(current_vector)) / (np.linalg.norm(target_vector) * np.linalg.norm(current_vector))

    r = projection / 2 + math.exp(-height_error * 0.0005) - 1 / 2

    return r


class Env:
    def __init__(self, fg2client_addr=("127.0.0.1", 5700), client2fg_addr=("127.0.0.1", 5701)):
        self.fg2client_addr = fg2client_addr
        self.client2fg_addr = client2fg_addr

        self.rece = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rece.bind(fg2client_addr)
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.baseline = 4000
        self.safe = False  # 0->system not ready for playing!; 1->system ready to mess with!

    def guard(self):
        """
        Guardian for fg, i.e., the pid controller
        Guardian automatically takes over when system is unsafe
        """
        while not self.safe:
            state = receiver(self.rece)
            self.safe = state['altitude'] > self.baseline+100
            action = pid(state)
            self.sender.sendto(action.encode("utf-8"), self.client2fg_addr)

    def reset(self):

        self.guard()

        dic = receiver(self.rece)
        df = pd.DataFrame(dic, index=[0])
        fea = df[['ai-offset', 'ai-pitch', 'ai-roll', 'airspeed-kt',
                  'alt-ft', 'altitude', 'down-accel-fps_sec', 'east-accel-fps_sec',
                  'flaps', 'heading-deg', 'hi-heading', 'latitude',
                  'longitude', 'north-accel-fps_sec', 'pitch-deg', 'roll-deg',
                  'speed-down-fps', 'speed-east-fps', 'speed-north-fps',
                  'uBody-fps', 'vBody-fps',
                  'vsi-fpm', 'wBody-fps', 'x-accel-fps_sec', 'y-accel-fps_sec',
                  'z-accel-fps_sec', 'aileron', 'elevator', 'rudder', 'throttle0', 'throttle1']]
        s = fea.values
        return s

    def step(self, action):
        """
        action is a numpy array with shape(1,5)
        The order is:
        aileron,elevator,rudder,throttle0,throttle1
        """
        control = "{0},{1},{2},{3},{4}\n".format(str(action[0, 0]), str(action[0, 1]), str(action[0, 2]),
                                                 str(action[0, 3]), str(action[0, 4]))
        self.sender.sendto(control.encode("utf-8"), self.client2fg_addr)

        dic = receiver(self.rece)
        df = pd.DataFrame(dic, index=[0])
        fea = df[['ai-offset', 'ai-pitch', 'ai-roll', 'airspeed-kt',
                  'alt-ft', 'altitude', 'down-accel-fps_sec', 'east-accel-fps_sec',
                  'flaps', 'heading-deg', 'hi-heading', 'latitude',
                  'longitude', 'north-accel-fps_sec', 'pitch-deg', 'roll-deg',
                  'speed-down-fps', 'speed-east-fps', 'speed-north-fps',
                  'uBody-fps', 'vBody-fps',
                  'vsi-fpm', 'wBody-fps', 'x-accel-fps_sec', 'y-accel-fps_sec',
                  'z-accel-fps_sec', 'aileron', 'elevator', 'rudder', 'throttle0', 'throttle1']]

        r = reward(dic)  # reward is in -1 to +1
        s = fea.values   # s(state) is a numpy array with shape(1,26)

        done = dic['altitude'] < self.baseline
        if done:
            self.safe = False

        return s, r, done
