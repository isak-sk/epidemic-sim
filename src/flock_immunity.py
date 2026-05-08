import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

N, I0, R0 = 1000, 1, 0
S0 = N - I0 - R0
t = np.linspace(0, 200, 200)

# Vi använder en lägre beta för att visa att inte alla blir smittade
beta, gamma = 0.15, 0.1

def deriv(y, t, N, beta, gamma):
    S, I, R = y
    return -beta * S * I / N, beta * S * I / N - gamma * I, gamma * I

ret = odeint(deriv, [S0, I0, R0], t, args=(N, beta, gamma))
S, I, R = ret.T

plt.figure(figsize=(10, 5))
plt.plot(t, S, label='Susceptible', color='#4FC3F7')
plt.plot(t, I, label='Infected', color='#EF5350')
plt.plot(t, R, label='Recovered', color='#66BB6A')
plt.axhline(y=S[-1], color='gray', linestyle='--', label=f'Återstående mottagliga: {int(S[-1])}')
plt.title("Demonstration av flockimmunitet")
plt.xlabel("Dagar")
plt.ylabel("Antal individer")
plt.legend()
plt.tight_layout()
plt.savefig("flockimmunitet.png", dpi=150)
