import numpy as np
import time
import random
import matplotlib.pyplot as plt

# -------------------------
# Problem Setup (Stochastic)
# -------------------------
omega_values = [0.3, 0.5, 0.7, 0.9]
phi_p_values = [1.0, 1.5, 2.0]
phi_g_values = [1.0, 1.5, 2.0]

original_priorities = [9000, 5000, 7000]
ai_priorities = [9500, 4800, 6600]

risks = [9, 4, 7]
distances = [3, 5, 6]
capacities = [20, 30, 10]

def objective(x):
    # Add noise to simulate stochastic environment
    noise = np.random.normal(0, 10)

    # Introduce slight random weights on priority importance per evaluation
    evac_weight = 1.0 + np.random.normal(0, 0.05)
    water_weight = 1.0 + np.random.normal(0, 0.05)
    fire_weight = 1.0 + np.random.normal(0, 0.05)

    # Adjusted priorities with weights
    adjusted_priorities = [
        x[0] * evac_weight,
        x[1] * water_weight,
        x[2] * fire_weight
    ]

    ai_error = sum((adjusted_priorities[i] - ai_priorities[i])**2 for i in range(3))
    original_error = sum((adjusted_priorities[i] - original_priorities[i])**2 for i in range(3))
    penalties = [
        0.5 * risks[i] + 0.3 * distances[i] + 0.2 * (100 / (capacities[i] + 1))
        for i in range(3)
    ]
    penalty_cost = sum(adjusted_priorities[i] * penalties[i] for i in range(3))

    return 0.4 * ai_error + 0.3 * original_error + 0.3 * penalty_cost + noise

# -------------------------
# Q-learning Setup
# -------------------------
actions = []
for o in range(len(omega_values)):
    for p in range(len(phi_p_values)):
        for g in range(len(phi_g_values)):
            actions.append((o, p, g))

action_counts = [0] * len(actions)

def discretize_state(gbest_improve, diversity):
    if gbest_improve > 1e-3:
        imp_state = 2
    elif gbest_improve > 1e-5:
        imp_state = 1
    else:
        imp_state = 0

    if diversity > 2000:
        div_state = 2
    elif diversity > 1000:
        div_state = 1
    else:
        div_state = 0

    return (imp_state, div_state)

q_table = {}
alpha = 0.1
gamma = 0.9
epsilon = 0.9  # initial, will decay

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

positions = np.random.uniform(0, 10000, (num_particles, num_dimensions))
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

    # Decaying epsilon
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
        positions[i] = np.clip(positions[i], 0, 10000)

        fitness = objective(positions[i])

        if fitness < pbest_values[i]:
            pbest_positions[i] = positions[i].copy()
            pbest_values[i] = fitness
            if fitness < gbest_value:
                gbest_position = positions[i].copy()
                gbest_value = fitness

    # Smarter reward signal
    if gbest_improve > 0:
        reward = gbest_improve
    else:
        reward = -0.01  # small penalty for no improvement

    # Add scaled diversity to reward
    reward += 0.0001 * swarm_diversity

    reward_history.append(reward)
    next_state = discretize_state(gbest_improve, swarm_diversity)
    update_q(state, action_idx, reward, next_state)

    if iteration % 5 == 0 or iteration == num_iterations - 1:
        print(f"Iter {iteration+1} | Best: {gbest_value:.2f} | ω:{omega:.2f} φp:{phi_p:.2f} φg:{phi_g:.2f} | Diversity:{swarm_diversity:.1f} | Reward:{reward:.4f}")

end_time = time.time()

# -------------------------
# Results
# -------------------------
print("\n✅ Optimal Balanced Priorities Found:")
print(f"Evacuation:       {gbest_position[0]:.2f}")
print(f"Water Gathering:  {gbest_position[1]:.2f}")
print(f"Fire Suppression: {gbest_position[2]:.2f}")
print(f"Total Cost:        {gbest_value:.2f}")
print(f"⏱ Time taken:     {end_time - start_time:.4f} seconds")

print("\n📊 Action usage summary (index, ω, φp, φg, count):")
sorted_actions = sorted(enumerate(action_counts), key=lambda x: -x[1])
for idx, count in sorted_actions:
    o, p, g = actions[idx]
    print(f"Action {idx}: ω={omega_values[o]:.2f}, φp={phi_p_values[p]:.2f}, φg={phi_g_values[g]:.2f} | Chosen {count} times")


