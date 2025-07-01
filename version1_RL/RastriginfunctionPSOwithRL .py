import numpy as np
import time
import random
import matplotlib.pyplot as plt

# -------------------------
# Problem Setup: Rastrigin Function
# -------------------------
def objective(x):
    n = len(x)
    A = 10
    return A * n + sum(x[i]**2 - A * np.cos(2 * np.pi * x[i]) for i in range(n))

# -------------------------
# RL hyperparameter action space
# -------------------------
omega_values = [0.3, 0.5, 0.7, 0.9]
phi_p_values = [1.0, 1.5, 2.0]
phi_g_values = [1.0, 1.5, 2.0]

actions = []
for o in range(len(omega_values)):
    for p in range(len(phi_p_values)):
        for g in range(len(phi_g_values)):
            actions.append((o, p, g))

action_counts = [0] * len(actions)

# -------------------------
# Q-learning Setup
# -------------------------
q_table = {}
alpha = 0.1
gamma = 0.9
epsilon = 0.9  # exploration rate, will decay

def discretize_state(gbest_improve, diversity):
    if gbest_improve > 1e-3:
        imp_state = 2
    elif gbest_improve > 1e-5:
        imp_state = 1
    else:
        imp_state = 0

    if diversity > 1.0:  # scale adjusted for Rastrigin
        div_state = 2
    elif diversity > 0.5:
        div_state = 1
    else:
        div_state = 0

    return (imp_state, div_state)

def get_q(state):
    if state not in q_table:
        q_table[state] = np.zeros(len(actions))
    return q_table[state]

def choose_action(state, eps):
    if random.random() < eps:
        return random.randint(0, len(actions) - 1)
    q_values = get_q(state)
    return np.argmax(q_values)

def update_q(state, action, reward, next_state):
    q_values = get_q(state)
    q_next = get_q(next_state)
    td_target = reward + gamma * np.max(q_next)
    td_delta = td_target - q_values[action]
    q_values[action] += alpha * td_delta

# -------------------------
# PSO Setup
# -------------------------
num_particles = 50
num_dimensions = 3
num_iterations = 100

# Initialize particles within Rastrigin domain [-5.12, 5.12]
positions = np.random.uniform(-5.12, 5.12, (num_particles, num_dimensions))
velocities = np.random.uniform(-1, 1, (num_particles, num_dimensions))

pbest_positions = positions.copy()
pbest_values = np.array([objective(p) for p in positions])

gbest_index = np.argmin(pbest_values)
gbest_position = pbest_positions[gbest_index].copy()
gbest_value = pbest_values[gbest_index]
prev_gbest_value = gbest_value

reward_history = []
start_time = time.time()

for iteration in range(num_iterations):
    swarm_diversity = np.mean(np.std(positions, axis=0))
    gbest_improve = prev_gbest_value - gbest_value
    prev_gbest_value = gbest_value

    state = discretize_state(gbest_improve, swarm_diversity)

    # Decay epsilon (exploration)
    epsilon = max(0.9 * (0.99 ** iteration), 0.1)

    action_idx = choose_action(state, epsilon)
    action_counts[action_idx] += 1
    omega_idx, phi_p_idx, phi_g_idx = actions[action_idx]
    omega = omega_values[omega_idx]
    phi_p = phi_p_values[phi_p_idx]
    phi_g = phi_g_values[phi_g_idx]

    for i in range(num_particles):
        r_p = np.random.rand(num_dimensions)
        r_g = np.random.rand(num_dimensions)

        velocities[i] = (
            omega * velocities[i] +
            phi_p * r_p * (pbest_positions[i] - positions[i]) +
            phi_g * r_g * (gbest_position - positions[i])
        )
        positions[i] = positions[i] + velocities[i]
        positions[i] = np.clip(positions[i], -5.12, 5.12)

        fitness = objective(positions[i])

        if fitness < pbest_values[i]:
            pbest_positions[i] = positions[i].copy()
            pbest_values[i] = fitness
            if fitness < gbest_value:
                gbest_position = positions[i].copy()
                gbest_value = fitness

    # Reward: positive if improved, small penalty if no improvement + small diversity bonus
    reward = gbest_improve if gbest_improve > 0 else -0.01
    reward += 0.001 * swarm_diversity

    reward_history.append(reward)
    next_state = discretize_state(gbest_improve, swarm_diversity)
    update_q(state, action_idx, reward, next_state)

    if iteration % 5 == 0 or iteration == num_iterations - 1:
        print(f"Iter {iteration+1} | Best: {gbest_value:.4f} | ω:{omega:.2f} φp:{phi_p:.2f} φg:{phi_g:.2f} | Diversity:{swarm_diversity:.4f} | Reward:{reward:.6f}")

end_time = time.time()

# -------------------------
# Results Summary
# -------------------------
print("\n✅ Optimal solution found:")
print(f"x = {gbest_position}")
print(f"Objective value = {gbest_value:.6f}")
print(f"⏱ Time taken: {end_time - start_time:.4f} seconds\n")

print("📊 Action usage (index, ω, φp, φg, count):")
sorted_actions = sorted(enumerate(action_counts), key=lambda x: -x[1])
for idx, count in sorted_actions:
    o, p, g = actions[idx]
    print(f"Action {idx}: ω={omega_values[o]:.2f}, φp={phi_p_values[p]:.2f}, φg={phi_g_values[g]:.2f} | Chosen {count} times")

# -------------------------
# Plot Reward History
# -------------------------
plt.figure(figsize=(10, 4))
plt.plot(reward_history, label="Reward")
plt.xlabel("Iteration")
plt.ylabel("Reward")
plt.title("Reward over Iterations (Rastrigin Benchmark)")
plt.grid(True)
plt.tight_layout()
plt.show()
