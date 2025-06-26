import numpy as np
import time

# Define the function to optimize
def sphere_function(x):
    return np.sum(x**2) + 42  # minimum value is 42 at x = 0

def rastrigin_function(x):
    A = 10
    n = len(x)
    return A * n + np.sum(x**2 - A * np.cos(2 * np.pi * x))

# PSO parameters
num_particles = 50    # number of particles
num_dimensions = 2    # dimensions of the problem
num_iterations = 100  # how many iterations to run

# PSO hyperparameters
omega = 0.5           # inertia weight (momentum)
phi_p = 1.5           # cognitive coefficient (particle's own experience)
phi_g = 1.5           # social coefficient (swarm experience)

# Initialize particle positions and velocities randomly
positions = np.random.uniform(-10, 10, (num_particles, num_dimensions))
velocities = np.random.uniform(-1, 1, (num_particles, num_dimensions))

# Initialize personal best positions and values
pbest_positions = positions.copy()
pbest_values = np.array([sphere_function(p) for p in positions])

# Initialize global best position and value
gbest_index = np.argmin(pbest_values)
gbest_position = pbest_positions[gbest_index]
gbest_value = pbest_values[gbest_index]

# Start timing
start_time = time.time()

for iteration in range(num_iterations):
    for i in range(num_particles):
        r_p = np.random.rand(num_dimensions)
        r_g = np.random.rand(num_dimensions)
        
        # Update velocity
        velocities[i] = (omega * velocities[i] +
                         phi_p * r_p * (pbest_positions[i] - positions[i]) +
                         phi_g * r_g * (gbest_position - positions[i]))
        
        # Update position
        positions[i] = positions[i] + velocities[i]
        
        # Evaluate fitness
        fitness = sphere_function(positions[i])
        
        # Update personal best if improved
        if fitness < pbest_values[i]:
            pbest_positions[i] = positions[i].copy()
            pbest_values[i] = fitness
            
            # Update global best if improved
            if fitness < gbest_value:
                gbest_position = positions[i].copy()
                gbest_value = fitness
    
    if iteration % 5 == 0 or iteration == num_iterations - 1:
        print(f"Iteration {iteration+1} - Best Value: {gbest_value:.4f}")

# End timing
end_time = time.time()
elapsed_time = end_time - start_time

print(f"\nOptimal position found: {gbest_position}")
print(f"Optimal value: {gbest_value:.4f}")
print(f"Time taken: {elapsed_time:.4f} seconds")
