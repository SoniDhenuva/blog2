import numpy as np
import time
import random

# -------------------------
# Problem Setup
# -------------------------
omega_values = [0.3, 0.5, 0.7, 0.9]
phi_p_values = [1.0, 1.5, 2.0]
phi_g_values = [1.0, 1.5, 2.0]

original_priorities = [9000, 5000, 7000]
ai_priorities = [9500, 4800, 6600]

risks = [9, 4, 7]
distances = [3, 5, 6]
capacities = [20, 30, 10]


# the function we arw optimizing, the lower the score the better--> gives a numerical score based on how close you are to what the AI said, old plan and how risky and difficult are the tasks you gave high priority?

def objective(x): #input is the list of number that are being tested for optimal purposes
    ai_error = sum((x[i] - ai_priorities[i])**2 for i in range(3))
    original_error = sum((x[i] - original_priorities[i])**2 for i in range(3))
    penalties = [
        0.5 * risks[i] + 0.3 * distances[i] + 0.2 * (100 / (capacities[i] + 1))
        for i in range(3)
    ]
    penalty_cost = sum(x[i] * penalties[i] for i in range(3))
    return 0.4 * ai_error + 0.3 * original_error + 0.3 * penalty_cost

# -------------------------
# Q-learning setup
# -------------------------
actions = [] # All possible combinations of omega values, phi_p_values, and phi_g_values
for o in range(len(omega_values)):
    for p in range(len(phi_p_values)):
        for g in range(len(phi_g_values)):
            actions.append( (o, p, g) )  # tuples of indices

# Simple discretized states based on (gbest_improvement, diversity)
def discretize_state(gbest_improve, diversity):
    # Discretize improvement
    if gbest_improve > 1e-3:
        imp_state = 2
    elif gbest_improve > 1e-5:
        imp_state = 1
    else:
        imp_state = 0
    # Discretize diversity (arbitrary cutoff)
    if diversity > 2000:
        div_state = 2
    elif diversity > 1000:
        div_state = 1
    else:
        div_state = 0
    return (imp_state, div_state)

q_table = {}  # {(state): [Q values for each action]}
alpha = 0.1   # learning rate
gamma = 0.9   # discount factor
epsilon = 0.2 # exploration rate

def get_q(state):
    if state not in q_table:
        q_table[state] = np.zeros(len(actions))
    return q_table[state]

def choose_action(state):
    if random.random() < epsilon:
        return random.randint(0, len(actions)-1)
    q_values = get_q(state)
    return np.argmax(q_values)

def update_q(state, action, reward, next_state):
    q_values = get_q(state)
    q_next = get_q(next_state)
    td_target = reward + gamma * np.max(q_next)
    td_delta = td_target - q_values[action]
    q_values[action] += alpha * td_delta

# -------------------------
# PSO parameters
# -------------------------
num_particles = 50
num_dimensions = 3
num_iterations = 100

# Initialize swarm positions and velocities
positions = np.random.uniform(0, 10000, (num_particles, num_dimensions))
velocities = np.random.uniform(-1, 1, (num_particles, num_dimensions))

pbest_positions = positions.copy()
pbest_values = np.array([objective(p) for p in positions])

gbest_index = np.argmin(pbest_values)
gbest_position = pbest_positions[gbest_index].copy()
gbest_value = pbest_values[gbest_index]

prev_gbest_value = gbest_value

start_time = time.time()

for iteration in range(num_iterations):
    # Calculate swarm diversity: mean std deviation over dimensions
    swarm_diversity = np.mean(np.std(positions, axis=0))
    
    # Calculate improvement in global best
    gbest_improve = prev_gbest_value - gbest_value
    prev_gbest_value = gbest_value
    
    # Discretize state
    state = discretize_state(gbest_improve, swarm_diversity)
    
    # Agent selects action (hyperparameters)
    action_idx = choose_action(state)
    omega_idx, phi_p_idx, phi_g_idx = actions[action_idx]
    omega = omega_values[omega_idx]
    phi_p = phi_p_values[phi_p_idx]
    phi_g = phi_g_values[phi_g_idx]
    
    # Run one PSO iteration with chosen hyperparameters
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
    
    # Reward = improvement in global best (positive better)
    reward = gbest_improve
    
    # Estimate next state (for simplicity use current state as next state, could compute next after move)
    next_state = discretize_state(gbest_improve, swarm_diversity)
    
    # Update Q-table
    update_q(state, action_idx, reward, next_state)
    
    if iteration % 5 == 0 or iteration == num_iterations - 1:
        print(f"Iter {iteration+1} | Best: {gbest_value:.2f} | ω:{omega:.2f} φp:{phi_p:.2f} φg:{phi_g:.2f} | Diversity:{swarm_diversity:.1f} | Reward:{reward:.4f}")

end_time = time.time()

print("\n Optimal Balanced Priorities Found:")
print(f"Evacuation:       {gbest_position[0]:.2f}")
print(f"Water Gathering:  {gbest_position[1]:.2f}")
print(f"Fire Suppression: {gbest_position[2]:.2f}")
print(f"Total Cost:        {gbest_value:.2f}")
print(f" Time taken:     {end_time - start_time:.4f} seconds")
