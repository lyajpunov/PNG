# -*- encoding: utf-8 -*-
"""
@File       :   main.py
@Contact    :   lyajpunov@hust.edu.cn
@Author     :   Li Yajun
@Time       :   2023/5/17$ 9:11$
@Version    :   1.0
@Desciption :   
"""

from model import missile, battle
import matplotlib.pyplot as plt

from settings import length

M0 = missile(0)
T0 = missile('T')
B = battle(M0, T0)

if __name__ == '__main__':
    for i in range(length - 10):
        a = 4 * M0.get_v() * B.get_dtheta_l()
        M0.step(a)
        T0.step(1)

        B.step()

        if B.get_r() < 1:
            print(B.get_r())
            break

plt.figure(1)
plt.plot(M0.x[:M0.pos], M0.y[:M0.pos])
plt.plot(T0.x[:T0.pos], T0.y[:T0.pos])
plt.xlabel('x')
plt.ylabel('y')
plt.legend(['M', 'T'])
plt.show()
