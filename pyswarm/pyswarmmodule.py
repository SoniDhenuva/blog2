# Importing necessary modules
from pyswarms.single import GlobalBestPSO
from pyswarms.utils.functions.single_obj import sphere

# Define the optimization problem
# The sphere function is already available in PySwarms
def sphere_function(x):
    return sphere(x)

# Number of dimensions (variables in the optimization problem)
n_dimensions = 2  # Let's optimize a 2D sphere function

# Define hyperparameters for the PSO algorithm
options = {
    'c1': 0.5,  # Cognitive parameter (personal influence)
    'c2': 0.3,  # Social parameter (swarm influence)
    'w': 0.9    # Inertia weight
}

# Create an instance of the GlobalBestPSO optimizer
optimizer = GlobalBestPSO(n_particles=10, dimensions=n_dimensions, options=options)

# Perform the optimization
best_cost, best_position = optimizer.optimize(sphere_function, iters=100)

# Display the results
print(f"Best cost (minimum value of the function): {best_cost}")
print(f"Best position (values of x at the minimum): {best_position}")
