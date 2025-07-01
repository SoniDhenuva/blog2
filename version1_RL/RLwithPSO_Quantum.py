import numpy as np
import time
import random

omega_values = [0.3, 0.5, 0.7, 0.9]
phi_p_values = [1.0, 1.5, 2.0]
phi_g_values = [1.0, 1.5, 2.0]

original_priorities = [9000, 5000, 7000]
ai_priorities = [9500, 4800, 6600]

risks = [9, 4, 7]
distances = [3, 5, 6]
capacities = [20, 30, 10]

def objective(x):
    ai_error = sum((x[i] - ai_priorities[i])**2 for i in range(3))
    original_error = sum((x[i] - original_priorities[i])**2 for i in range(3))
    penalties = [
        0.5 * risks[i] + 0.3 * distances[i] + 0.2 * (100 / (capacities[i] + 1))
        for i in range(3)
    ]
    penalty_cost = sum(x[i] * penalties[i] for i in range(3))
    return 0.4 * ai_error + 0.3 * original_error + 0.3 * penalty_cost

actions = [(o, p, g) for o in range(len(omega_values)) for p in range(len(phi_p_values)) for g in range(len(phi_g_values))]
action_counts = [0] * len(actions)

def discretize_state(gbest_improve, diversity):
    imp_state = 2 if gbest_improve > 1e-3 else 1 if gbest_improve > 1e-5 else 0
    div_state = 2 if diversity > 2000 else 1 if diversity > 1000 else 0
    return (imp_state, div_state)

q_table = {}
alpha = 0.1
gamma = 0.9
epsilon = 0.9  

def get_q(state):
    if state not in q_table:
        q_table[state] = np.zeros(len(actions))
    return q_table[state]

def choose_action(state, eps):
    return random.randint(0, len(actions) - 1) if random.random() < eps else np.argmax(get_q(state))

def update_q(state, action, reward, next_state):
    q_values = get_q(state)
    td_target = reward + gamma * np.max(get_q(next_state))
    q_values[action] += alpha * (td_target - q_values[action])

def form_clusters(fitness_values, threshold=500):
    clusters = []
    sorted_indices = np.argsort(fitness_values)
    current_cluster = [sorted_indices[0]]

    for i in sorted_indices[1:]:
        if abs(fitness_values[i] - fitness_values[current_cluster[-1]]) < threshold:
            current_cluster.append(i)
        else:
            clusters.append(current_cluster)
            current_cluster = [i]
    clusters.append(current_cluster)
    return clusters

def apply_adaptive_coupling(positions, velocities, clusters, diversity, max_strength=0.5):
    coupling_strength = np.clip(max_strength * (2000 / (diversity + 1e-5)), 0.05, max_strength)
    for cluster in clusters:
        if len(cluster) <= 1:
            continue
        cluster_positions = positions[cluster]
        cluster_velocities = velocities[cluster]

        centroid_pos = np.mean(cluster_positions, axis=0)
        centroid_vel = np.mean(cluster_velocities, axis=0)

        for idx in cluster:
            vel_influence = coupling_strength * (centroid_vel - velocities[idx])
            pos_influence = 0.05 * coupling_strength * (centroid_pos - positions[idx])
            velocities[idx] += vel_influence + pos_influence

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

   
    clusters = form_clusters(pbest_values, threshold=500)
    apply_adaptive_coupling(positions, velocities, clusters, swarm_diversity)

    
    positions += velocities
    positions = np.clip(positions, 0, 10000)

    for i in range(num_particles):
        fitness = objective(positions[i])
        if fitness < pbest_values[i]:
            pbest_positions[i] = positions[i].copy()
            pbest_values[i] = fitness
            if fitness < gbest_value:
                gbest_position = positions[i].copy()
                gbest_value = fitness

    reward = gbest_improve if gbest_improve > 0 else -0.01
    reward += 0.0001 * swarm_diversity
    reward_history.append(reward)

    next_state = discretize_state(gbest_improve, swarm_diversity)
    update_q(state, action_idx, reward, next_state)

    if iteration % 5 == 0 or iteration == num_iterations - 1:
        print(f"Iter {iteration+1} | Best: {gbest_value:.2f} | ω:{omega:.2f} φp:{phi_p:.2f} φg:{phi_g:.2f} | Diversity:{swarm_diversity:.1f} | Reward:{reward:.4f}")

end_time = time.time()

print("\n Optimal Balanced Priorities Found:")
print(f"Evacuation:       {gbest_position[0]:.2f}")
print(f"Water Gathering:  {gbest_position[1]:.2f}")
print(f"Fire Suppression: {gbest_position[2]:.2f}")
print(f"Total Cost:        {gbest_value:.2f}")
print(f"Time taken:     {end_time - start_time:.4f} seconds")
