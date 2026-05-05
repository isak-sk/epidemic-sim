import numpy as np
import matplotlib.pyplot as plt

def simulate_vaccination(vax_rate):
    N, steps = 300, 400
    inf_rad, inf_prob, rec_steps, speed = 0.02, 0.4, 80, 0.005
    states = np.full(N, 0)
    # Vaccinera en andel av befolkningen direkt
    vax_count = int(N * vax_rate)
    vax_idx = np.random.choice(N, vax_count, replace=False)
    states[vax_idx] = 2 
    # Starta smitta bland de icke-vaccinerade
    remaining = np.where(states == 0)[0]
    states[np.random.choice(remaining, 3, replace=False)] = 1
    
    pos = np.random.rand(N, 2)
    timer = np.zeros(N)
    hist = []
    for _ in range(steps):
        pos = (pos + np.random.uniform(-speed, speed, (N, 2))) % 1.0
        inf_idx, sus_idx = np.where(states == 1)[0], np.where(states == 0)[0]
        if len(inf_idx) > 0 and len(sus_idx) > 0:
            for s in sus_idx:
                if np.any(np.linalg.norm(pos[s] - pos[inf_idx], axis=1) < inf_rad) and np.random.rand() < inf_prob:
                    states[s] = 1
        timer[states == 1] += 1
        states[(states == 1) & (timer >= rec_steps)] = 2
        hist.append(np.sum(states == 1))
    return hist

plt.figure(figsize=(10, 5))
plt.plot(simulate_vaccination(0.0), label='0% Vaccinerade', color='#EF5350')
plt.plot(simulate_vaccination(0.4), label='40% Vaccinerade', color='#66BB6A')
plt.title("Simulering av vaccinationsstrategi")
plt.xlabel("Tidssteg")
plt.ylabel("Antal smittade")
plt.legend()
plt.tight_layout()
plt.savefig("vaccination_test.png", dpi=150)
