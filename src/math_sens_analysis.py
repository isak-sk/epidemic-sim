import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

N = 1000
I0, R0 = 1, 0
S0 = N - I0 - R0
gamma = 0.1
t = np.linspace(0, 160, 160)

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    return -beta * S * I / N, beta * S * I / N - gamma * I, gamma * I

# Vi testar fyra olika beta-värden för att se känsligheten
betas = [0.15, 0.25, 0.4, 0.6]
plt.figure(figsize=(10, 6))

for b in betas:
    y0 = S0, I0, R0
    ret = odeint(deriv, y0, t, args=(N, b, gamma))
    S, I, R = ret.T
    plt.plot(t, I, label=f'Smittsamhet (beta) = {b}')

plt.title('Känslighetsanalys: Hur beta påverkar epidemins topp')
plt.xlabel('Dagar')
plt.ylabel('Antal smittade (I)')
plt.grid(alpha=0.3)
plt.legend()
plt.savefig("kanslighetsanalys.png", dpi=150)
