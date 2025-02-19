from pyswarm import pso

# Example function that simulates getting desired priorities from user input.
def get_desired_priorities():
    # These would typically be updated dynamically based on terminal inputs.
    # For instance, if "fire is near people", then evacuation is high priority.
    desired_evacuation = 9000  # highest priority
    desired_water = 5000      # medium priority
    desired_fire = 7000       # moderately high priority
    return [desired_evacuation, desired_water, desired_fire]

# Define the objective function for PSO
def objective(x):
    # x[0]: evacuation, x[1]: water gathering, x[2]: fire suppression
    desired = get_desired_priorities()
    weights = [1, 1, 1]
    # Compute the squared error between candidate and desired priorities
    cost = (weights[0]*(x[0] - desired[0]) ** 2 + weights[1]*(x[1] - desired[1]) ** 2 +weights[0]*(x[2] - desired[2]) ** 2) # desired[0] = 1, desired[1] = 0.5
    #print(f"Cost: {cost} (Desired: {desired}, Candidate: {x})")
    return cost

# Lower and upper bounds for each task's priority
lb = [0, 0, 0]  # Lower bounds (min priority)
ub = [10000, 10000, 10000]  # Upper bounds (max priority)

# PSO Parameters (Inertia weight, cognitive and social factors)
omega = 0.3  # Lower inertia weight (more sensitive to changes)
phip = 3.0  # Higher cognitive factor (more personal exploration)
phig = 3.0  # Higher social factor (more influence from the swarm)

# Run the Particle Swarm Optimization
optimal_priorities, optimal_cost = pso(objective, lb, ub, swarmsize=20, maxiter=150, omega=0.3, phip=3.0, phig = 3.0)


print("Optimal Task Priorities (Evacuation, Water, Fire Suppression):", optimal_priorities)
print("Cost at Optimal Priorities:", optimal_cost)

# Example function to assign tasks based on optimized priorities
def assign_tasks_to_drones(optimal_priorities):
    # For demonstration purposes, just print the task assignments
    tasks = ["Evacuation", "Water Gathering", "Fire Suppression"]
    for task, priority in zip(tasks, optimal_priorities):
        print(f"Assigning task '{task}' with priority {priority:.2f}")

assign_tasks_to_drones(optimal_priorities)

def main():
    import time
    while True:
        user_input = input("Enter update (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        # In a real system, update desired priorities based on user input.
        # For example, parse input and adjust parameters accordingly.
        # Here, we just call our function for demonstration.
        
        # Re-run optimization to get new task priorities
        optimal_priorities, optimal_cost = pso(objective, lb, ub, swarmsize=20, maxiter=150, omega=0.3, phip=3.0, phig = 3.0)
        print("\nUpdated Optimal Task Priorities:", optimal_priorities)
        print("Updated Cost:", optimal_cost)
        assign_tasks_to_drones(optimal_priorities)

        
        # Wait a moment before next iteration (simulate continuous operation)
        time.sleep(1)

if __name__ == '__main__':
    main()


