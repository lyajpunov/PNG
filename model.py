# -*- encoding: utf-8 -*-
"""
@File       :   model.py
@Contact    :   lyajpunov@hust.edu.cn
@Author     :   Li Yajun
@Time       :   2023/5/17$ 9:11$
@Version    :   1.0
@Desciption :
"""

import numpy as np
from settings import dt, length, data


class missile:
    def __init__(self, name):
        self.pos = 0
        self.name = name
        self.length = length
        # x轴位置
        self.x = np.zeros(self.length, dtype='float64')
        # y轴位置
        self.y = np.zeros(self.length, dtype='float64')
        # 速度
        self.v = np.zeros(self.length, dtype='float64')
        # 弹道倾角
        self.theta = np.zeros(self.length, dtype='float64')
        # 控制量：加速度
        self.a = np.zeros(self.length, dtype='float64')
        # 停止标志位
        self.end = False
        # 初始化，重置
        self.reset()

    def reset(self):
        self.pos = 0
        self.x[self.pos] = data[self.name]['x']
        self.y[self.pos] = data[self.name]['y']
        self.v[self.pos] = data[self.name]['v']
        self.theta[self.pos] = np.deg2rad(data[self.name]['theta'])

    def step(self, a):
        # 如果已经结束直接返回
        if self.end:
            return

        # 保存控制量
        self.a[self.pos] = a

        # 形成向量进行迭代
        vector = np.array([self.x[self.pos],
                           self.y[self.pos],
                           self.v[self.pos],
                           self.theta[self.pos],
                           self.a[self.pos], ])
        k1 = dt * self.iterateOnce(vector)
        k2 = dt * self.iterateOnce(vector + 0.5 * k1)
        k3 = dt * self.iterateOnce(vector + 0.5 * k2)
        k4 = dt * self.iterateOnce(vector + k3)
        vector = vector + (k1 + 2 * k2 + 2 * k3 + k4) / 6

        # 保存迭代数据
        self.pos += 1
        self.x[self.pos] = vector[0]
        self.y[self.pos] = vector[1]
        self.v[self.pos] = vector[2]
        self.theta[self.pos] = vector[3]

    def iterateOnce(self, vector):
        x, y, v, theta, a = vector[0], vector[1], vector[2], vector[3], vector[4]

        _x = v * np.cos(theta)
        _y = v * np.sin(theta)
        _v = 0
        _theta = a / v
        _a = 0

        return np.array([_x, _y, _v, _theta, _a])

    '''以下为接口函数'''
    def get_x(self):
        return self.x[self.pos]

    def get_y(self):
        return self.y[self.pos]

    def get_v(self):
        return self.v[self.pos]

    def get_a(self):
        return self.a[self.pos]

    def get_theta(self):
        return self.theta[self.pos]


class battle:
    def __init__(self, M, T):
        self.pos = 0
        self.M = M
        self.T = T
        self.length = length
        # 距离及其导数
        self.r = np.zeros(self.length, dtype='float64')
        self.dr = np.zeros(self.length, dtype='float64')
        # 视线倾角及其导数
        self.theta_l = np.zeros(self.length, dtype='float64')
        self.dtheta_l = np.zeros(self.length, dtype='float64')
        # 初始化
        self.reset()

    def reset(self):
        self.pos = 0
        d_x = self.T.get_x() - self.M.get_x()
        d_y = self.T.get_y() - self.M.get_y()
        d_vx = self.T.get_v() * np.cos(self.T.get_theta()) - self.M.get_v() * np.cos(self.M.get_theta())
        d_vy = self.T.get_v() * np.sin(self.T.get_theta()) - self.M.get_v() * np.sin(self.M.get_theta())

        r = np.sqrt(d_x * d_x + d_y * d_y)
        d_r = (d_x * d_vx + d_y * d_vy) / r
        theta_l = np.arctan(d_y / d_x)
        dtheta_l = d_x * d_x * (d_vy * d_x - d_vx * d_y) / (r * r) / (d_vx * d_vx)

        self.r[self.pos] = r
        self.dr[self.pos] = d_r
        self.theta_l[self.pos] = theta_l
        self.dtheta_l[self.pos] = dtheta_l

    def step(self):
        self.pos += 1

        d_x = self.T.get_x() - self.M.get_x()
        d_y = self.T.get_y() - self.M.get_y()
        d_vx = self.T.get_v() * np.cos(self.T.get_theta()) - self.M.get_v() * np.cos(self.M.get_theta())
        d_vy = self.T.get_v() * np.sin(self.T.get_theta()) - self.M.get_v() * np.sin(self.M.get_theta())

        r = np.sqrt(d_x * d_x + d_y * d_y)
        d_r = (d_x * d_vx + d_y * d_vy) / r
        theta_l = np.arctan(d_y / d_x)
        dtheta_l = d_x * d_x * (d_vy * d_x - d_vx * d_y) / (r * r) / (d_vx * d_vx)

        self.r[self.pos] = r
        self.dr[self.pos] = d_r
        self.theta_l[self.pos] = theta_l
        self.dtheta_l[self.pos] = dtheta_l

    '''下面是接口函数'''
    def get_r(self):
        return self.r[self.pos]

    def get_dr(self):
        return self.dr[self.pos]

    def get_theta_l(self):
        return self.theta_l[self.pos]

    def get_dtheta_l(self):
        return self.dtheta_l[self.pos]
