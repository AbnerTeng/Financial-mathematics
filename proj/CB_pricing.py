# %%
import polars as pl
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import os
import sys
from numpy import exp as e
from numpy import sqrt as sqrt

stock = yf.download('2338.TW', start = '2020-08-03', end = '2021-08-03')
close = stock['Close']

plt.style.use('seaborn')
plt.plot(close, label = '2338.TW')
plt.legend()
plt.show()

'''define parameters'''
S = np.zeros([1000, 1250])
P = np.zeros(1250)
P0 = 115230
C_v = np.array([88.8] * 1250)
M = 100000
r = 0.015
sigma = close.pct_change().std()
dt = 1/250
V = []
C = np.zeros(1250)

'''Bond price'''
for t in range(1, 1251):
    P[-t] = M * e(-r * dt * (t-1))

'''call price'''
C0 = P0 - P[0]
de = C0 / len(P)
for t in range(1250):
    C[t] = C0 - de * (t + 1)

'''Monte Carlo Simulation'''
C_r = (C + P)/M
for N in range(1000):
    S_0 = close[-1] ## S_0 is the first value of close price

    for t in range(1250):
        dW_t = np.random.normal(0, np.sqrt(dt))
        S[N, t] = S_0 * e((r - 0.5 * sigma ** 2) * dt + sigma * dW_t)

        if S[N, t] > C_v[t] * C_r[t] and t > 0.25*250:
            V.append(((S[N, t] - C_v[t] * C_r[t]) * e(-r*dt*t)) + P[0])
            break
        elif t == 1249:
            V.append(P[0] + C[0])
        else:
            S_0 = S[N, t]


'''fig1'''
plt.style.use('ggplot')
plt.figure(figsize = (20, 10))
for i in range(1250):
    plt.plot(S[i])
plt.xticks(np.arange(0, 1250, 50), np.arange(0, 5, 0.2))
plt.show()
# %%
'''V'''
print(np.mean(V))
premium_ratio = (P0 - np.mean(V))/P0 * 100
print(f'premium ratio: {premium_ratio:.2f}%')

'''fig2'''
plt.style.use('ggplot')
plt.figure(figsize = (20, 10))
plt.plot(V, label = 'V')
plt.legend()
plt.show()
# %%
