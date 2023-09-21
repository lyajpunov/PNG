# -*- encoding: utf-8 -*-
"""
@File       :   settings.py
@Contact    :   lyajpunov@hust.edu.cn
@Author     :   Li Yajun
@Time       :   2023/5/17$ 9:15$
@Version    :   1.0
@Desciption :   
"""

# 最长仿真时间
t = 100
# 仿真步长
dt = 1e-3
# 预留数组长度
length = int(t / dt)

data = {
    0: {
        'x': 0,
        'y': 0,
        'v': 300,
        'theta': 0,
    },

    'T': {
        'x': 10000,
        'y': 10000,
        'v': 50,
        'theta': 0,
    },
}
