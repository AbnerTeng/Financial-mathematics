# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from math import sqrt

TSMC = yf.download('2330.TW', start='2020-01-01', end='2022-10-31')
TSMC['return'] = TSMC['Close'].pct_change()
TSMC['log_return'] = np.log(TSMC['Close']/TSMC['Close'].shift(1))
sigma = TSMC['return'].std()
log_sigma = TSMC['log_return'].std()
X0 = TSMC['Close'][0]
mu = TSMC['return'].mean()
log_mu = TSMC['log_return'].mean()

N = 1000
h = 1
temp = np.zeros([N, len(TSMC)])
X_return = np.zeros([len(TSMC)])
X_return[0] = X0

for i in range(N):
    for t in range(len(TSMC)-1):
        epsilon = np.random.normal(0, 1)
        X_return[t+1] = (X_return[t]*np.exp((mu - 0.5*sigma**2)*h + sigma*sqrt(h)*epsilon))
    temp[i, :] = X_return
TSMC['X_return'] = X_return

for i in range(N):
    plt.plot(temp[i])

fig = plt.figure(figsize=(18,10)) 
plt.plot(TSMC['X_return']) 
plt.plot(TSMC['Close']) 
plt.title('Simulation',fontsize='16') 
plt.xlabel('Period(Day)',fontsize='16') 
plt.ylabel('Price',fontsize='16') 
plt.legend(['Simulations','True']) 
plt.show()


fx = yf.download("TWD=X", start = '2020-01-01', end = '2022-10-31')
Y0 = fx['Close'][0]
fx['return'] = fx['Close'].pct_change()
fx['log_return'] = np.log(fx['Close']/fx['Close'].shift(1))
Sigma = fx['return'].std()
log_Sigma = fx['log_return'].std()
Mu = fx['return'].mean()
log_Mu = fx['log_return'].mean()

N = 1000
h = 1
Temp = np.zeros([N, len(fx)])
Y_return = np.zeros([len(fx)])
Y_return[0] = Y0

for i in range(N):
    for t in range(len(fx)-1):
        epsilon = np.random.normal(0, 1, 1000)
        Y_return[t+1] = (Y_return[t]*np.exp((Mu - 0.5*Sigma**2)*h + Sigma*sqrt(h)*epsilon[t]))
    fx['Y_return'] = Y_return
    Temp[i, :] = Y_return

for i in range(N):
    plt.plot(Temp[i])


fig = plt.figure(figsize=(18,10)) 
plt.plot(fx['Y_return']) 
plt.plot(fx['Close']) 
plt.title('Simulation',fontsize='16') 
plt.xlabel('Period(Day)',fontsize='16') 
plt.ylabel('Price',fontsize='16') 
plt.legend(['Simulations','True']) 
plt.show()
# %%
