import numpy as np 
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Parameters
N = 1000        # Total population
I0 = 1          # Initial infected
R0 = 0          # Initial recovered
S0 = N - I0 - R0 # Initial susceptible
beta = 0.3      # Transmission rate
gamma = 0.1     # Recovery rate
t = np.linspace(0, 160, 160) # Time grid (days)

# SIR Model Differential Equations
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# Integrate Equations
y0 = S0, I0, R0
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, R = ret.T

# Plot Results
plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.legend()

plt.savefig("SIR.png", dpi=150, bbox_inches="tight")
