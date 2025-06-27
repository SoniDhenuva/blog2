import numpy as np
import time

# -------------------------
# Problem Setup
# -------------------------
# Priorities (can come from AI or user input)
original_priorities = [9000, 5000, 7000]
ai_priorities = [9500, 4800, 6600]

# Task characteristics
risks = [9, 4, 7]         # Higher = more critical
distances = [3, 5, 6]     # Higher = farther
capacities = [20, 30, 10] # Higher = better

# -------------------------
# Objective Function
# -------------------------
def objective(x):
    # Normalize x if needed (optional, not mandatory here)
    ai_error = sum((x[i] - ai_priorities[i])**2 for i in range(3))
    original_error = sum((x[i] - original_priorities[i])**2 for i in range(3))

    # Penalty from risk, distance, capacity
    penalties = [
        0.5 * risks[i] + 0.3 * distances[i] + 0.2 * (100 / (capacities[i] + 1))
        for i in range(3)
    ]
    penalty_cost = sum(x[i] * penalties[i] for i in range(3))

    # Combine all with weights (you can tune these!)
    return (
        0.4 * ai_error +          # prioritize AI suggestions
        0.3 * original_error +    # still respect original
        0.3 * penalty_cost        # penalize bad assignments
    )

# -------------------------
# PSO Parameters
# -------------------------
num_particles = 50
num_dimensions = 3  # 3 tasks
num_iterations = 100

omega = 0.5
phi_p = 1.5
phi_g = 1.5

# Initialize particle positions and velocities
positions = np.random.uniform(0, 10000, (num_particles, num_dimensions))
velocities = np.random.uniform(-1, 1, (num_particles, num_dimensions))

# Initialize personal bests
pbest_positions = positions.copy()
pbest_values = np.array([objective(p) for p in positions])

# Global best
gbest_index = np.argmin(pbest_values)
gbest_position = pbest_positions[gbest_index]
gbest_value = pbest_values[gbest_index]

# -------------------------
# Run PSO
# -------------------------
start_time = time.time()

for iteration in range(num_iterations):
    for i in range(num_particles):
        r_p = np.random.rand(num_dimensions)
        r_g = np.random.rand(num_dimensions)
        
        # Update velocity and position
        velocities[i] = (
            omega * velocities[i] +
            phi_p * r_p * (pbest_positions[i] - positions[i]) +
            phi_g * r_g * (gbest_position - positions[i])
        )
        positions[i] = positions[i] + velocities[i]
        positions[i] = np.clip(positions[i], 0, 10000)  # keep in range
        
        # Evaluate
        fitness = objective(positions[i])
        
        # Update personal/global bests
        if fitness < pbest_values[i]:
            pbest_positions[i] = positions[i].copy()
            pbest_values[i] = fitness
            if fitness < gbest_value:
                gbest_position = positions[i].copy()
                gbest_value = fitness

    if iteration % 5 == 0 or iteration == num_iterations - 1:
        print(f"Iteration {iteration+1} - Best Value: {gbest_value:.2f}")

end_time = time.time()

# -------------------------
# Results
# -------------------------
print("\n✅ Optimal Balanced Priorities Found:")
print(f"Evacuation:       {gbest_position[0]:.2f}")
print(f"Water Gathering:  {gbest_position[1]:.2f}")
print(f"Fire Suppression: {gbest_position[2]:.2f}")
print(f"Total Cost:        {gbest_value:.2f}")
print(f"⏱️ Time taken:     {end_time - start_time:.4f} seconds")
