import numpy as np
import matplotlib.pyplot as plt

def run_abm_logic(seed_value):
    np.random.seed(seed_value)
    # Parametrar från din ursprungliga kod
    N, steps, speed = 300, 400, 0.003
    infection_radius, infection_prob, recovery_steps = 0.015, 0.35, 80
    
    states = np.full(N, 0); states[np.random.choice(N, 3, replace=False)] = 1
    positions = np.random.rand(N, 2)
    infected_timer = np.zeros(N)
    recovery_time = (recovery_steps * np.random.uniform(0.7, 1.3, N)).astype(int)
    
    i_hist = []
    for t in range(steps):
        # Enkel rörelse och smitta (förkortad logik för bilden)
        positions = (positions + np.random.uniform(-speed, speed, (N, 2))) % 1.0
        inf_idx, sus_idx = np.where(states == 1)[0], np.where(states == 0)[0]
        if len(inf_idx) > 0 and len(sus_idx) > 0:
            for s in sus_idx:
                dists = np.linalg.norm(positions[s] - positions[inf_idx], axis=1)
                if np.any(dists < infection_radius) and np.random.rand() < infection_prob:
                    states[s] = 1
        # Återhämtning
        inf_mask = states == 1
        infected_timer[inf_mask] += 1
        states[inf_mask & (infected_timer >= recovery_time)] = 2
        i_hist.append(np.sum(states == 1))
    return i_hist

# Kör tre olika frön för att visa variation
plt.figure(figsize=(10, 6))
seeds = [42, 7, 123] # Olika slumpfrön
for s in seeds:
    data = run_abm_logic(s)
    plt.plot(data, label=f'Körning (Seed {s})')

plt.title('Stokastiska effekter: Samma parametrar, olika utfall')
plt.xlabel('Tidssteg')
plt.ylabel('Antal smittade (I)')
plt.legend()
plt.savefig("stokastisk_variation.png", dpi=150)
